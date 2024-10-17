from threading import Thread
import time

def print_numbers(values: list[float]) -> None:
    for i, v in enumerate(values):
        print(v)
        if i == len(values) - 1:
            break
        time.sleep(1)

def supervisor():
    numbers = [1,2,3,4,5,6,7,8,9,10]

    threads : list[Thread] = []

    threads_count = 3

    for _ in range(threads_count):
        thread = Thread(target=print_numbers, args=[numbers])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main() -> None:
    supervisor()

if __name__ == '__main__':
    main()