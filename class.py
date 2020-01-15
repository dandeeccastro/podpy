class MyClass:
    def __init__(self,name=None):
        if name is not None:
            self.name = name
        else:
            self.name = 'Alberto'

x = MyClass()
y = MyClass('Juau')
print(x.name)
print(y.name)

