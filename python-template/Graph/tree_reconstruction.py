def _validate(first, inorder):
    """Validate two unique traversal sequences."""
    if len(first) != len(inorder) or len(set(inorder)) != len(inorder) or set(first) != set(inorder):
        raise ValueError('traversals must contain the same unique values')


def build_from_preorder_inorder(preorder, inorder):
    """Return (root, left, right) maps from preorder and inorder traversals."""
    preorder, inorder = list(preorder), list(inorder)
    _validate(preorder, inorder)
    if not preorder:
        return None, {}, {}
    position = {value: index for index, value in enumerate(inorder)}
    left_child, right_child = {}, {}

    def build(in_left, in_right, pre_left):
        """Build one traversal slice and return its root value."""
        root = preorder[pre_left]
        middle = position[root]
        if not in_left <= middle < in_right:
            raise ValueError('inconsistent traversals')
        left_size = middle - in_left
        if left_size:
            left_child[root] = build(in_left, middle, pre_left + 1)
        if middle + 1 < in_right:
            right_child[root] = build(middle + 1, in_right, pre_left + left_size + 1)
        return root

    root = build(0, len(inorder), 0)
    return root, left_child, right_child


def build_from_postorder_inorder(postorder, inorder):
    """Return (root, left, right) maps from postorder and inorder traversals."""
    postorder, inorder = list(postorder), list(inorder)
    _validate(postorder, inorder)
    if not postorder:
        return None, {}, {}
    position = {value: index for index, value in enumerate(inorder)}
    left_child, right_child = {}, {}

    def build(in_left, in_right, post_right):
        """Build one traversal slice and return its root value."""
        root = postorder[post_right - 1]
        middle = position[root]
        if not in_left <= middle < in_right:
            raise ValueError('inconsistent traversals')
        right_size = in_right - middle - 1
        if middle > in_left:
            left_child[root] = build(in_left, middle, post_right - right_size - 1)
        if right_size:
            right_child[root] = build(middle + 1, in_right, post_right - 1)
        return root

    root = build(0, len(inorder), len(postorder))
    return root, left_child, right_child
