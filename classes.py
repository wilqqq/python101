class Empty:
    pass

class Person():
    raise_amount = 1.04
    number_of_emps = 0
    def __init__(self, name, surname="Newbie"):
        self.name = name
        Person.number_of_emps +=1
        print("This is {}, employee number {}".format(self.name, self.number_of_emps))
    def fun(self):
        print("every function needs a positional argument {} (instance)".format(self))
    def apply_raise(self):
        self.pay = int(self.pay * Person.raise_amount)
    @staticmethod
    def is_workday(day): # do not need object nor class
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
    @classmethod #decorator
    def set_raise_amount(cls, amount): #cls is like self in methods
        cls.raise_amount = amount
    @classmethod
    def from_string(cls, emp_str):
        f, l = emp_str.split('-')
        return cls(f, l) #returning a new object

class Superhero(Person):
    pass

kuba = Person("Kuba")#, end=" ::__[+]__:: ")

Person.raise_amount = 1.05 # change for all instances
kuba.raise_amount = 1.07 # change for only kuba
kuba.fun()
Person.fun(kuba) # two lines doing the same thing

Karol = Person.from_string("Karol-Dlawik")

import datetimels
my_date = datetime.date(2016, 7, 10)
print(Person.is_workday(my_date))

print("henlo how are you? %5.2f" % (123.456))
print("print formating {} {}".format("thus", "cuz"))

l = [i**3 + 2*i + 16 for i in range(-5,35)] #inline list
r = (-i for i in range(1,100)) #inline generator

p = [i*j for j in range(100) for i in range(100)]

with open('data.txt','w') as f:
    f.write(str(p))