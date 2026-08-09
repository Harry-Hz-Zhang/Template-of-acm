def inversion_count(values):
    """Run the inversion count operation."""
    compressed = {value: index + 1 for index, value in enumerate(sorted(set(values)))}
    tree = [0] * (len(compressed) + 1)

    def add(index):
        """Run the add operation."""
        while index < len(tree):
            tree[index] += 1
            index += index & -index

    def prefix(index):
        """Run the prefix operation."""
        result = 0
        while index:
            result += tree[index]
            index -= index & -index
        return result

    answer = 0
    for processed, value in enumerate(values):
        index = compressed[value]
        answer += processed - prefix(index)
        add(index)
    return answer
