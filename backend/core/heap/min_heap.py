class MinHeap:
    """Binary min-heap used as a priority queue.

    Stores (priority, item) pairs in an array-backed complete binary tree
    where every parent has a priority lower than or equal to its children,
    so the minimum is always at index 0.

    Ties between equal priorities are broken by insertion order (FIFO),
    which keeps algorithms such as Dijkstra deterministic and avoids ever
    comparing the stored items themselves.

    Complexity: push O(log n), pop O(log n), peek O(1).
    """

    def __init__(self):
        """Create an empty heap.

        Receives: nothing.
        Returns:
            None.
        How it works:
            ``_items`` holds tuples (priority, sequence, item); ``_sequence``
            is a counter that increases on every push to break ties.
        """
        self._items = []
        self._sequence = 0

    def push(self, priority: float, item) -> None:
        """Insert an item with the given priority.

        Receives:
            priority: number used to order the items (lower comes first).
            item: any value to store.
        Returns:
            None.
        How it works:
            Appends the entry at the end of the array and moves it up
            (sift up) while it is smaller than its parent.
        """
        self._items.append((priority, self._sequence, item))
        self._sequence += 1
        self._sift_up(len(self._items) - 1)

    def pop(self) -> tuple:
        """Remove and return the entry with the lowest priority.

        Receives: nothing.
        Returns:
            tuple: (priority, item) of the minimum entry.
        How it works:
            Swaps the root with the last element, removes it and moves the
            new root down (sift down) until the heap property holds again.
        Raises:
            IndexError: if the heap is empty.
        """
        if self.is_empty():
            raise IndexError("cannot pop from an empty heap")
        last_index = len(self._items) - 1
        self._swap(0, last_index)
        priority, _, item = self._items.pop()
        if self._items:
            self._sift_down(0)
        return priority, item

    def peek(self) -> tuple:
        """Return the entry with the lowest priority without removing it.

        Receives: nothing.
        Returns:
            tuple: (priority, item) of the minimum entry.
        Raises:
            IndexError: if the heap is empty.
        """
        if self.is_empty():
            raise IndexError("cannot peek an empty heap")
        priority, _, item = self._items[0]
        return priority, item

    def is_empty(self) -> bool:
        """Tell whether the heap has no entries.

        Receives: nothing.
        Returns:
            bool: True if the heap is empty.
        """
        return not self._items

    def size(self) -> int:
        """Return the number of stored entries.

        Receives: nothing.
        Returns:
            int: amount of entries.
        """
        return len(self._items)

    def _sift_up(self, index: int) -> None:
        """Move an entry up until its parent is not greater.

        Receives:
            index: position of the entry to move.
        Returns:
            None.
        How it works:
            The parent of ``i`` is ``(i - 1) // 2``; while the entry is lower
            than its parent both are swapped.
        """
        while index > 0:
            parent = (index - 1) // 2
            if self._items[index] >= self._items[parent]:
                return
            self._swap(index, parent)
            index = parent

    def _sift_down(self, index: int) -> None:
        """Move an entry down until both children are not lower.

        Receives:
            index: position of the entry to move.
        Returns:
            None.
        How it works:
            The children of ``i`` are ``2i + 1`` and ``2i + 2``; the entry is
            swapped with its lowest child while that child is lower.
        """
        size = len(self._items)
        while True:
            smallest = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < size and self._items[child] < self._items[smallest]:
                    smallest = child
            if smallest == index:
                return
            self._swap(index, smallest)
            index = smallest

    def _swap(self, first: int, second: int) -> None:
        """Swap two positions of the internal array.

        Receives:
            first, second: indexes to swap.
        Returns:
            None.
        """
        self._items[first], self._items[second] = self._items[second], self._items[first]
