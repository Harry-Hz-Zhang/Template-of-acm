class TimestampXorBasis(object):
    """Query whether value is representable using vectors with timestamp >= minimum."""

    def __init__(self, max_bit=60):
        """Initialize the data structure."""
        self.vector = [0] * (max_bit + 1)
        self.timestamp = [-1] * (max_bit + 1)

    def insert(self, value, timestamp):
        """Run the insert operation."""
        for bit in range(len(self.vector) - 1, -1, -1):
            if not (value >> bit) & 1:
                continue
            if self.vector[bit] == 0:
                self.vector[bit] = value
                self.timestamp[bit] = timestamp
                return True
            if timestamp > self.timestamp[bit]:
                value, self.vector[bit] = self.vector[bit], value
                timestamp, self.timestamp[bit] = self.timestamp[bit], timestamp
            value ^= self.vector[bit]
        return False

    def can_represent(self, value, minimum_timestamp=0):
        """Run the can represent operation."""
        for bit in range(len(self.vector) - 1, -1, -1):
            if (value >> bit) & 1:
                if self.timestamp[bit] < minimum_timestamp:
                    return False
                value ^= self.vector[bit]
        return True
