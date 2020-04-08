import re
import string
from copy import deepcopy


class SingletonMeta(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Designs(list, metaclass=SingletonMeta):

    def add_design(self, spec):
        self.append((BouquetDesign(spec)))

    def pop(self, index=None):
        try:
            return super().pop(index)
        except IndexError:
            return


class FlowerWarehouse(dict, metaclass=SingletonMeta):

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self["L"] = {k: 0 for k in list(string.ascii_lowercase)}
        self["S"] = {k: 0 for k in list(string.ascii_lowercase)}

    def add_flower(self, size, specie):
        self[size][specie] += 1


class BouquetDesign:

    def __init__(self, spec):
        self.specification = spec
        self.name = spec[0]
        self.size = spec[1]
        self.flowers, self.total_qty, self.additional_qty = self._parse_spec()

    def __repr__(self):
        return self.specification

    def _parse_spec(self):
        """
        Split bouquet specification on the separated parts

        :param spec: example 'AL10a15b5c30'
        :return: lowers in bouquet, total quantity of flowers, additional free space
        """
        result = re.findall("(\d*\w)", self.specification[2:])
        total_qty = int(result.pop(len(result) - 1))
        flowers = [{'qty': int(i[1]), 'specie': i[2]} for i in map(lambda x: re.split("(\d+)", x), result)]
        additional_qty = total_qty - sum(v['qty'] for v in flowers)
        return flowers, total_qty, additional_qty


class Bouquet:
    NEW = 1
    REQUIRED = 2
    ADDITIONAL = 3
    DONE = 4

    def __init__(self, design):
        self.design = design
        self.final = ''
        self.required_flowers = deepcopy(design.flowers)
        self.additional_qty = design.additional_qty
        self.flowers = {}
        self.status = self.NEW

    def __repr__(self):
        return f'{self.final}'

    @property
    def is_ready(self):
        return self.status == self.DONE

    async def create_by_specification(self):
        """
        Create bouquet by specifications
        """
        pool = FlowerWarehouse()[self.design.size]

        for flower in self.required_flowers:
            qty = flower['qty']
            specie = flower['specie']
            if specie not in self.flowers:
                self.flowers[specie] = 0

            if not pool[specie]:
                continue

            if qty > pool[specie]:
                self.flowers[specie] += pool[specie]
                flower['qty'] -= pool[specie]
                pool[specie] = 0
            else:
                self.flowers[specie] += qty
                pool[specie] -= qty
                self.required_flowers.remove(flower)

        if not len(self.required_flowers):
            self.status += 1

    async def add_additional_flowers(self):
        """
        Add free flowers to free space in the bouquet
        """
        if self.status != self.REQUIRED:
            return
        pool = FlowerWarehouse()[self.design.size]

        for specie, f_qty in pool.items():
            if not self.additional_qty:
                break

            if not f_qty:
                continue

            if specie not in self.flowers:
                self.flowers[specie] = 0

            if self.additional_qty >= f_qty:
                self.flowers[specie] += f_qty
                self.additional_qty -= f_qty
            else:
                self.flowers[specie] += self.additional_qty
                pool[specie] -= self.additional_qty
                self.additional_qty = 0

        if not self.additional_qty:
            self.status += 1
            return

    async def gather_bouquet(self):
        """
        Gather all flowers in the one bouquet
        """
        if self.status != self.ADDITIONAL:
            return

        self.final = f'{self.design.name}{self.design.size}'
        for k, v in sorted(self.flowers.items()):
            self.final = f'{self.final}{v}{k}'
        self.status += 1
