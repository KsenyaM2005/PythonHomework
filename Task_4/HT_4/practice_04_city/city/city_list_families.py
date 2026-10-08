from city.person import Person
from city.city import City
from city.city_list import CityList


class Relatives:
    def __init__(self):
        self.mother = None       # индекс матери или None
        self.father = None       # индекс отца или None
        self.children = []       # список индексов детей

    def __str__(self):
        return "mother={}, father={}, children={}".format(
            self.mother, self.father, self.children
        )


class CityListFamilies(CityList):
    def __init__(self, name: str, count: int):
        super().__init__(name, count)
        self._relatives_dict = {}



    def add_person(self, p: Person):
        if not City.add_person(self):
            return None
        self._person_list.append(p)
        idx = len(self._person_list) - 1
        self._relatives_dict[idx] = Relatives()
        return idx



    def remove_person(self, idx: int) -> bool:
        if idx < 0 or idx >= len(self._person_list):
            return False
        if not City.remove_person(self):
            return False

        del self._person_list[idx]
        del self._relatives_dict[idx]
        self._reindex_after_removal(idx)
        return True


    def _reindex_after_removal(self, removed_idx: int) -> None:
        new_rel = {}
        for old_idx, rel in self._relatives_dict.items():
            new_idx = old_idx - 1 if old_idx > removed_idx else old_idx

            if rel.mother is not None:
                if rel.mother == removed_idx:
                    rel.mother = None
                elif rel.mother > removed_idx:
                    rel.mother -= 1

            if rel.father is not None:
                if rel.father == removed_idx:
                    rel.father = None
                elif rel.father > removed_idx:
                    rel.father -= 1

            rel.children = [
                c - 1 if c > removed_idx else c
                for c in rel.children if c != removed_idx
            ]
            new_rel[new_idx] = rel
        self._relatives_dict = new_rel



    def set_parents(self, child_idx: int,
                    mother_idx=None,
                    father_idx=None) -> bool:
        n = len(self._person_list)
        if not (0 <= child_idx < n):
            return False
        if mother_idx is not None and not (0 <= mother_idx < n):
            return False
        if father_idx is not None and not (0 <= father_idx < n):
            return False

        rel = self._relatives_dict[child_idx]
        if mother_idx is not None:
            rel.mother = mother_idx
            self._relatives_dict[mother_idx].children.append(child_idx)
        if father_idx is not None:
            rel.father = father_idx
            self._relatives_dict[father_idx].children.append(child_idx)
        return True



    def get_relatives(self, idx: int):
        return self._relatives_dict.get(idx)



    def get_person(self, idx: int):
        if 0 <= idx < len(self._person_list):
            return self._person_list[idx]
        return None


    def __str__(self) -> str:
        s = [super().__str__()]
        s.append("\nRelatives map:\n")
        for idx in sorted(self._relatives_dict):
            s.append("  [{}] {} -> {}\n".format(
                idx, self._person_list[idx], self._relatives_dict[idx]
            ))
        return ''.join(s)