try:
    num_1 = int(input("Num 1: "))
    num_2 = int(input("Num 2: "))
    result = num_1 / num_2

except ZeroDivisionError:
    print("error: zero division")
    
else:
    print(result)