from multiprocessing import Process, Manager


def factorial(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_in_process(i: int, dict, n: int) -> None:
    dict[i] = factorial(n)


def supervisor() -> None:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    manager = Manager()
    result_dict = manager.dict()
    processes: list[Process] = []
    for i, v in enumerate(numbers):
        process = Process(target=factorial_in_process,
                          args=[i, result_dict, v])
        process.start()
        processes.append(process)

    for p in processes:
        p.join()

    print(result_dict.values())


def main() -> None:
    supervisor()


if __name__ == '__main__':
    main()
