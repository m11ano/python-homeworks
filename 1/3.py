class NoEvenNumbers(Exception):
    pass

class NoNegativeNumbers(Exception):
    pass

try:
    nums_list =[int(x) for x in input("Numbers list: ").split()]

    for n in nums_list:
        if n < 0:
            raise NoNegativeNumbers(f"number {n} is negative")
        if n % 2 == 0:
            raise NoEvenNumbers(f"number {n} is even")
        
except ValueError:
    print("error: correct integer numeric values should be entered")
except (NoEvenNumbers, NoNegativeNumbers) as e:
    print(f"error: {e}")

else:
    print("Its okey!")