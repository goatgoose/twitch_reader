
class Test:
    def __init__(self, value):
        self.value = 10

    def copy(self):
        new = self.__init__(self.value)
        return new


class Child(Test):
    def __init__(self, value):
        super().__init__(value)
        self.value2 = 20


if __name__ == '__main__':
    t = Child(10)
    print(t.value2)
    t2 = t.copy()
    t2.value2 = 21
    print(t2.value2)

