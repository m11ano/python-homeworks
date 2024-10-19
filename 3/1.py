from threading import Thread
from typing import TypeVar, Generic

T = TypeVar("T")


class ThreadWithReturn(Generic[T]):
    __result: T
    __thread: Thread

    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
    ):
        def targetDef():
            self.__result = target(*args)

        self.__thread = Thread(
            group, targetDef, name, args=(), kwargs=None, daemon=daemon
        )

    def start(self) -> None:
        self.__thread.start()

    def join(self) -> T:
        self.__thread.join()
        return self.__result


def count_number_power(values: list[float], power: float) -> list[float]:
    values = values.copy()
    for i, v in enumerate(values):
        values[i] = v**power

    return values


def supervisor() -> None:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    power_2_thread = ThreadWithReturn[list[float]](
        target=count_number_power, args=(numbers, 2)
    )
    power_2_thread.start()

    power_3_thread = ThreadWithReturn[list[float]](
        target=count_number_power, args=(numbers, 3)
    )
    power_3_thread.start()

    list_2 = power_2_thread.join()
    list_3 = power_3_thread.join()

    print(list_2)
    print(list_3)


def main() -> None:
    supervisor()


if __name__ == "__main__":
    main()
