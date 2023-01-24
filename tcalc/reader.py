from collections import deque


class InputReader:
    def __init__(self, source: str) -> None:
        self._queue = deque(source)
        self._column = 0

    def peek(self) -> tuple[str, int]:
        return self._queue[1], self._column

    def next(self) -> tuple[str, int]:
        self._column += 1
        return self._queue.popleft(), self._column

    def isEOF(self) -> bool:
        return len(self._queue) == 0
