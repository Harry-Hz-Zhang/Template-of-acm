class TraceableXorBasis(object):
    def __init__(self, max_bit=60):
        """Initialize the data structure."""
        self.vector = [0] * (max_bit + 1)
        self.trace = [0] * (max_bit + 1)

    def insert(self, value, item_id):
        """Run the insert operation."""
        trace = 1 << item_id
        for bit in range(len(self.vector) - 1, -1, -1):
            if not (value >> bit) & 1:
                continue
            if self.vector[bit]:
                value ^= self.vector[bit]
                trace ^= self.trace[bit]
            else:
                self.vector[bit] = value
                self.trace[bit] = trace
                return True
        return False

    def represent(self, value):
        """Run the represent operation."""
        trace = 0
        for bit in range(len(self.vector) - 1, -1, -1):
            if (value >> bit) & 1:
                if not self.vector[bit]:
                    return None
                value ^= self.vector[bit]
                trace ^= self.trace[bit]
        return [index for index in range(trace.bit_length()) if (trace >> index) & 1]
