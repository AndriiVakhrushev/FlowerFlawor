from bouquet_design.models import Bouquet, Designs, FlowerWarehouse


class BouquetCreator:

    def __init__(self):
        self.designs = Designs()
        self.flower_warehouse = FlowerWarehouse()

    async def apply_design(self, design):
        return Bouquet(design)

    async def create_bouquet(self, bouquet):
        await bouquet.create_by_specification()
        await bouquet.add_additional_flowers()
        await bouquet.gather_bouquet()
        return bouquet
