from abc import ABC, abstractmethod
import random
import time
import math


class Vector2D():
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def getComponents(self):
        return [self._x, self._y]

    def abs(self):
        return math.sqrt(self._x * self._x + self._y * self._y)

    def cdot(self, param):
        return self._x * param.getComponents()[0] + self._y * param.getComponents()[1]


class Box:
    _n = 0
    _m = 0
    def __init__(self, n, m):
        Box._n = n
        Box._m = m


class RandomState:
    def randomstate(self):
        return random.random()


class Person(Vector2D):
    def __init__(self, start_speed=1.0):
        edge = random.randint(1, 4)
        if edge == 1:
            super().__init__(random.uniform(0, Box._n), 0)
        elif edge == 2:
            super().__init__(Box._n, random.uniform(0, Box._m))
        elif edge == 3:
            super().__init__(random.uniform(0, Box._n), Box._m)
        elif edge == 4:
            super().__init__(0, random.uniform(0, Box._m))

        self._speed = start_speed

        self._objawystate = "Brak - Zdrowy"
        if RandomState.randomstate(self) <= 0.5:
            self._startstate = "Odporny"
            self._healthstate = "Zdrowy"
        else:
            self._startstate = "Wrażliwy"
            # było 5% teraz jest 10% (0.1 -> 0.2)
            if RandomState.randomstate(self) <= 0.2:
                self._healthstate = "Zakażony"
                if RandomState.randomstate(self) <= 0.5:
                    self._objawystate = "Posiada objawy"
                else:
                    self._objawystate = "Nie posiada objawów"
            else:
                self._healthstate = "Zdrowy"

        self._zakazonytime = 0.0
        self._odpornosctime = random.uniform(20, 30)

        self._distancetable = dict()

        print(self._healthstate)

    def change_coords(self, direction):
        # North
        if (direction == 1):
            self._y = self._y + self._speed
            # East
        elif (direction == 2):
            self._x = self._x + self._speed
        # South
        elif (direction == 3):
            self._y = self._y - self._speed
        # West
        elif (direction == 4):
            self._x = self._x - self._speed

    def check_boundries(self):
        # Check if boundries were reached
        if (Box._n < self._x or self._x < 0):
            # Zawracanie do wewnątrz
            if (random.randint(0, 1) == 0):
                if self._x > 0:
                    self._x = Box._n
                else:
                    self._x = 0
            # Wyjście z obszaru
            else:
                return "Exit"

        if (Box._m < self._y or self._y < 0):
            if (random.randint(0, 1) == 0):
                if self._y > 0:
                    self._y = Box._m
                else:
                    self._y = 0
            else:
                return "Exit"

    def movement(self):
        self._speed = random.uniform(0, 2.5)
        self.change_coords(random.randint(1, 4))

    def distance(self, second_person):
        return math.sqrt((second_person._x - self._x) ** 2 + (second_person._y - self._y) ** 2)

    def change_objawystate(self):
        if random.randint(0, 1) == 0 and self._startstate != "Odporny":
            self._healthstate = "Zakażony"
            if RandomState.randomstate() <= 0.5:
                self._objawystate = "Posiada objawy"
            else:
                self._objawystate = "Nie posiada objawów"

    def count_zakazonytime(self):
        if self._healthstate == "Zakażony":
            self._zakazonytime += 0.04
        else:
            self._zakazonytime = 0.0

    def getodpornosc(self):
        if self._zakazonytime >= self._odpornosctime:
            self._startstate = "Odporny"
            self._healthstate = "Zdrowy"
            self._zakazonytime = 0.0
            self._objawystate = "Brak - Zdrowy"

    def check3stime(self, personobj, persontime):
        if persontime == 3.0:
            self._healthstate = "Zakażony"
            if RandomState.randomstate() <= 0.5:
                self._objawystate = "Posiada objawy"
            else:
                self._objawystate = "Nie posiada objawów"
            self._distancetable[personobj] = 0.0


plane = Box(10, 10)
person_table = [Person() for i in range(0, 5)]
delete_id = list()

# init tablicy czasów
for person in person_table:
    for i in range(0, len(person_table)):
        if person == person_table[i]:
            continue
        person._distancetable[person_table[i]] = 0.0

counter = 0

for x in range(0, 31):
    for step in range(0, 25):
        counter += 1
        id = random.randint(0, len(person_table) - 1)
        person = person_table[id]
        person.count_zakazonytime()
        person.getodpornosc()
        if (person.check_boundries() == "Exit"):
            print("Wyszedł z obszaru")
            delete_id.append(id)
        else:
            person.movement()
            print(f"person_id: {id}, step: {counter}, health: {person._healthstate}, objawy: {person._objawystate}")
        for i in range(0, len(person_table) - 1):
            if person_table[i] == person:
                continue
            if person.distance(person_table[i]) <= 2 and person._startstate == "Wrażliwy" and person_table[i]._healthstate == "Zakażony":
                person._distancetable[person_table[i]] += 0.04

                person.check3stime(person_table[i], person._distancetable[person_table[i]])
                if person_table[i]._objawystate == "Nie posiada objawów":
                    person.change_objawystate()
                else:
                    person._healthstate = "Zakażony"
            elif person.distance(person_table[i]) > 2:
                person._distancetable[person_table[i]] = 0.0
        if len(delete_id) != 0 :
            for ids in delete_id:
                for person in person_table:
                    if person_table[ids] == person:
                        continue
                    # czasami dochodzi no nadpisania (osobnik trafia do swojego distancetable)
                    del person._distancetable[person_table[ids]]
                del person_table[ids]
                for n in range(0, len(delete_id)):
                    delete_id[n] = delete_id[n] - 1
            delete_id.clear()

        # dochodzi nowy osobnik 30% szans
        if random.random() <= 0.1 or len(person_table) < 4:
            print("Tworzenie nowego osobnika")
            new_person = Person()

            person_table.append(new_person)
            for person in person_table:
                person._distancetable[new_person] = 0.0