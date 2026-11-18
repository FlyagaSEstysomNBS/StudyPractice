import asyncio
import time


async def get_courier_status(name, delay):
    await asyncio.sleep(delay)
    statuses = {
        "A": "в пути",
        "Б": "на складе",
        "В": "доставил"
    }
    return f"Курьер {name}: {statuses.get(name, "неизвестно")}"

async def main():
    start_time = time.perf_counter()
    results = await asyncio.gather(
        get_courier_status("А", 1.0),
        get_courier_status("Б", 1.0),
        get_courier_status("В", 1.0)
    )
    end_time = time.perf_counter()
    total_time = end_time - start_time

    for res in results:
        print(res)
    
    print(f"Общее время: {total_time:.2f} сек")


if __name__ == "__main__":
    asyncio.run(main())