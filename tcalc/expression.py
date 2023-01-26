from decimal import Decimal
from typing import Any, Union


class Time:
    """
    TIME EXPRESSION

      A Time Expression represents a duration in time.
      It is defined as

        [+-]?[H]:[M]:[S]

      with

        H as hours,
        M as minutes,
        S as seconds.

      H, M and S are unsigned Integers.

    TIME EXPRESSION ARITHMETIC

      The following operations are legal:

        * Addition
        * Subtraction
        * Multiplication
        * Division.

      Addition and Subtraction must be applied to another Time Expression.
      Multiplication and Division must be applied to positive Integers
      or Floats.

    EXAMPLES

      Add 12 seconds to a full hour:
        > 1:: + ::12
        = 01:00:12

      Multiply one hour, 34 minutes and 20 seconds with 4:
        > 1:34:20 * 4
        = 06:17:20

      Convert 666 seconds to a wellformed format:
        > 0:0:666
        = 00:11:06
    """

    def __init__(self, hours: Decimal, minutes: Decimal, seconds: Decimal):
        self.hour = hours
        self.minute = minutes
        self.second = seconds
        self.fmt = "{:0>2}:{:0>2}:{:0>2}"

    def time2sec(self) -> Decimal:
        r = Decimal("0")
        r += self.hour * 3600
        r += self.minute * 60
        r += self.second
        return r

    def sec2time(self, s: Decimal) -> "Time":
        h, s = divmod(s, 3600)
        m, s = divmod(s, 60)
        return Time(h, m, s)

    def __str__(self) -> str:
        t = self.sec2time(self.time2sec())  # avoid malformed time
        return self.fmt.format(t.hour, t.minute, t.second)

    __repr__ = __str__

    def __add__(self, other: "Time") -> "Time":
        t1 = self.time2sec()
        t2 = other.time2sec()
        return self.sec2time(t1 + t2)

    def __sub__(self, other: "Time") -> "Time":
        t1 = self.time2sec()
        t2 = other.time2sec()
        return self.sec2time(t1 - t2)

    def __mul__(self, other: Decimal) -> "Time":
        t = self.time2sec()
        return self.sec2time(t * other)

    __rmul__ = __mul__

    def __truediv__(self, other: Union[Decimal, "Time"]) -> Union[Decimal, "Time"]:
        if isinstance(other, Decimal):
            t = self.time2sec()
            return self.sec2time(t / other)
        elif isinstance(other, Time):
            t1 = self.time2sec()
            t2 = other.time2sec()
            return t1 / t2
        else:
            raise ValueError("Unsupported operand {}".format(other))

    def __rtruediv__(self, other: Any) -> None:
        raise ValueError("Divison not allowed for {}".format(other))

    def __neg__(self) -> "Time":
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Time):
            return self.time2sec() == other.time2sec()
        return False
