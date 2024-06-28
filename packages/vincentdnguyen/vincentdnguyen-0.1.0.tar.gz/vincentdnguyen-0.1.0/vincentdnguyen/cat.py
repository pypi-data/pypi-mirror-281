class Cat:
    def __init__(self, name):
        self.__name = name
        
    def describe(self):
        print(self.__name)