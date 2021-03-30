
class CropData:
    def __init__(self, year: int, crop_area: float, crop_area_detail: dict = None):
        self.year = year
        self.crop_area = crop_area
        self.crop_area_detail = crop_area_detail

    def __str__(self):
        return f"CropData(year={self.year}, crop_area={self.crop_area}, crop_area_detail={str(self.crop_area_detail)})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CropData):
            raise NotImplemented()
        if self.year != o.year:
            return False
        if self.crop_area != o.crop_area:
            return False
        if self.crop_area_detail != o.crop_area_detail:
            return False
        return True

    def __hash__(self) -> int:
        hash_val = hash(self.year) + hash(self.crop_area)
        for crop_detail in self.crop_area_detail.items():
            hash_val += hash(crop_detail[0]) + hash(crop_detail[1])
        return hash_val


class DevelopedArea:
    def __init__(self, year: int, area: float):
        self.year = year
        self.area = area

    def __str__(self):
        return f"DevelopedArea(year={self.year}, area={self.area})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, DevelopedArea):
            raise NotImplemented()
        if self.year != o.year:
            return False
        if self.area != o.area:
            return False
        return True

    def __hash__(self) -> int:
        hash_val = hash(self.year) + hash(self.area)
        return hash_val
