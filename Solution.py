#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: T
    left: Optional["Node[T]"] = None
    right: Optional["Node[T]"] = None


class Tree(Generic[T]):
    def __init__(self) -> None:
        # HackerRank runtime error fix: always define root.
        self.root: Optional[Node[T]] = None

    def insert(self, value: T) -> None:
        def helper(node: Optional[Node[T]], v: T) -> Node[T]:
            if node is None:
                return Node(v)
            if v < node.value:
                node.left = helper(node.left, v)
            else:
                node.right = helper(node.right, v)
            return node

        self.root = helper(self.root, value)

    def print_ordered(self) -> str:
        out: list[str] = []

        def inorder(node: Optional[Node[T]]) -> None:
            if node is None:
                return
            inorder(node.left)
            out.append(str(node.value))
            inorder(node.right)

        inorder(self.root)
        return " ".join(out)

    def is_balanced(self) -> bool:
        def height_or_unbalanced(node: Optional[Node[T]]) -> int:
            if node is None:
                return 0
            lh = height_or_unbalanced(node.left)
            if lh < 0:
                return -1
            rh = height_or_unbalanced(node.right)
            if rh < 0:
                return -1
            if abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)

        return height_or_unbalanced(self.root) >= 0

    def __str__(self) -> str:
        return self.print_ordered()


def main() -> None:
    """
    Simple CLI harness for local testing.

    Many HackerRank problems provide their own harness; in that case, only the
    Tree/Node implementation above matters.
    """
    import sys

    data = [int(x) for x in sys.stdin.read().strip().split()]
    if not data:
        return

    i = 0
    trees: list[Tree[int]] = []
    while i < len(data):
        n = data[i]
        i += 1
        t = Tree[int]()
        for _ in range(n):
            if i >= len(data):
                break
            t.insert(data[i])
            i += 1
        trees.append(t)

    for t in trees:
        sys.stdout.write(t.print_ordered() + "\n")
        sys.stdout.write("true\n" if t.is_balanced() else "false\n")


if __name__ == "__main__":
    main()

