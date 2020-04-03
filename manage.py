import asyncio
from aioconsole import ainput

from bouquet_design.comsumer import Consumer
from bouquet_design.creator import BouquetCreator
from bouquet_design.models import Designs


async def run_consumer():
    # '/usr/src/bloomon/sample.txt'
    consumer = Consumer()
    while True:
        # await consumer.handle(input())
        await consumer.handle(await ainput())


async def run_factory():
    bouquets = set()
    while True:
        creator = BouquetCreator()
        design = Designs().pop(0)
        if design:
            bouquets.add(await creator.apply_design(design))

        if len(bouquets):
            bouquet = bouquets.pop()
            await creator.create_bouquet(bouquet)
            if bouquet.is_ready:
                print(bouquet)
            else:
                bouquets.add(bouquet)
        await asyncio.sleep(0.01)

if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    ioloop.create_task(run_consumer())
    ioloop.create_task(run_factory())
    try:
        print("Service started. Enter path to file or designs and flowers to console")
        ioloop.run_forever()
    except KeyboardInterrupt:
        pass
