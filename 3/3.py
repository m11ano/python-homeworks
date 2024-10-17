import asyncio

async def count_number_power(value: float, power : float) -> float:
    await asyncio.sleep(1)
    return value**power

async def supervisor() -> None:
    numbers = [1,2,3,4,5,6,7,8,9,10]
    tasks = []
    for v in numbers:
        tasks.append(asyncio.create_task(count_number_power(v, 2)))

    result = await asyncio.gather(*tasks)
    print(result)

def main() -> None:
    asyncio.run(supervisor())

if __name__ == '__main__':
    main()