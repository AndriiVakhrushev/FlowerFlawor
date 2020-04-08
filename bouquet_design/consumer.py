from bouquet_design.models import Designs, FlowerWarehouse
from aiofile import AIOFile, LineReader


class Consumer:

    async def handle(self, arg):
        arg = arg.strip()
        if not arg:
            return
        if arg.endswith('txt'):
            await self._read_from_file(arg)
        else:
            for a in arg.replace('\\t', '').split('\\n'):
                await self._add_field(a)

    async def _read_from_file(self, path):
        async with AIOFile(path, "r")as f:
            async for row in LineReader(f):
                await self._add_field(row)

    async def _add_field(self, row):
        row = row.strip()
        if len(row) < 1:
            return
        if len(row) > 2:
            Designs().add_design(row)
        else:
            if row[1] not in FlowerWarehouse():
                print(f'Wrong  flower size. "{row[1]}"')
                return
            FlowerWarehouse().add_flower(row[1], row[0])
