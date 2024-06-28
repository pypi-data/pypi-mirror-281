def type_vars():
    class Person:
        title = "title111"

        def __init__(self, name, age):
            self.name = name
            self.age = age

        @property
        def is_adult(self):
            return self.age >= 18

    p = Person("Alice", 25)
    print("1 p                  :", p)  # <__main__.Person object at 0x0000015E20FECFD0>
    print("2 p.is_adult         :", p.is_adult)  # True
    print("3 vars(p)            :", vars(p))  ## {'name': 'Alice', 'age': 25}
    print("4 vars(Person)       :", vars(Person))  ## {'__module__': '__main__', 'title': 'title111', '__init__': <function Person.__init__ at 0x0000022FCD71F670>, 'is_adult': <property object at 0x0000022FCD72F860>,
    print("5 type(vars(Person)) :", type(vars(Person)))  ## <class 'mappingproxy'>
    print("6 type(vars(Person)) :", vars(Person)['species'])


if __name__ == '__main__':
    type_vars()
