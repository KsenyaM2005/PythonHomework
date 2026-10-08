import sys

from city.person import Person
from city.city import  City
from city.city_list import CityList
from city.city_list_families import CityListFamilies

def city_list_families_test() -> None:
    c4 = CityListFamilies("City_with_families", 10)

    mom = Person("Anna", "Ivanova", "Petrovna")
    dad = Person("Ivan", "Ivanov", "Sergeevich")
    son = Person("Petr", "Ivanov", "Ivanovich")
    daughter = Person("Maria", "Ivanova", "Ivanovna")

    i_mom = c4.add_person(mom)        # 0
    i_dad = c4.add_person(dad)        # 1
    i_son = c4.add_person(son)        # 2
    i_daughter = c4.add_person(daughter)  # 3

    print("Индексы:", i_mom, i_dad, i_son, i_daughter)

    c4.set_parents(i_son, mother_idx=i_mom, father_idx=i_dad)
    c4.set_parents(i_daughter, mother_idx=i_mom, father_idx=i_dad)

    print(c4)

    print("Relatives of son:", c4.get_relatives(i_son))
    print("Relatives of mom:", c4.get_relatives(i_mom))

    c4.remove_person(i_dad)

    print("\nПосле удаления отца:\n")
    print(c4)

    print("Relatives of son:", c4.get_relatives(1))   # сын теперь под индексом 1
    print("Relatives of mom:", c4.get_relatives(0))   # мать осталась под 0
    

if __name__ == '__main__':

    print("Program is started \n")

    city_list_families_test()


    print("Program is finished \n")


