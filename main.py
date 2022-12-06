from __future__ import annotations

import random
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits
import math

class Vector2D():
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def getComponents(self):
        return [self._x, self._y]

    def setComponents(self, x, y):
        self._x = x
        self._y = y

    def abs(self):
        return math.sqrt(self._x * self._x + self._y * self._y)

    def cdot(self, param):
        return self._x * param.getComponents()[0] + self._y * param.getComponents()[1]

class Person(Vector2D):
    _health_options = ["odporny", "zdrowy", "objawy", "bez objawow"]
    _state = None
    def __init__(self, state: str, x: float, y: float) -> None:
        #stan
        self._state = state
        self._position = Vector2D(x, y)
        self._speed = random.uniform(0, 2.5)
        self._health = 0
        self._direction = Vector2D(0, 0)

    def movement(self):
        self._speed = random.uniform(0, 2.5)
        #random direction
        if(random.random() <= 0.5):
             self._direction.setComponents(0, )
        else:
            pass

    def do_something(self) -> None:
        print("Person is doing smth important")
        self._state = self._generate_random_string(30)
        print(f"Person: my state has changed to: {self._state}")
    def save(self) -> Memento:
        return ConcreteMemento(self._state)

    def restore(self, memento: Memento) -> None:
        self._state = memento.get_state()
        print(f"Restoring to state: {self._state}")
    def _generate_random_string(self, length: int = 10) -> None:
        return "".join(sample(ascii_letters, length))

class Box:
    _n = 0
    _m = 0
    def __init__(self, n = 10, m = 10):
        Box._n = n
        Box._m = m
class Memento(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

class ConcreteMemento(Memento):
    def __init__(self, state: str) -> None:
        self._state = state
        self._date = str(datetime.now())[:19]

    def get_state(self) -> str:
        return self._state
    def get_name(self) -> str:
        return f"{self._date} / ({self._state[0:9]}...)"
    def get_date(self) -> str:
        return self._date

class CareTaker:
    def __init__(self, person: Person) -> None:
        self._mementos = []
        self._person = person

    def backup(self) -> None:
        print("\nCaretaker: Saving Originator's state...")
        self._mementos.append(self._person.save())

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print(f"Caretaker: Restoring state to: {memento.get_name()}")
        try:
            self._person.restore(memento)
        except Exception:
            self.undo()
    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos: ")
        for memento in self._mementos:
            print(memento.get_name())


if __name__ == "__main__":
    pass
#po kazdej sekundzie zapisz state na personie
