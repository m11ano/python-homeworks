numbers = list(range(0, 10))

try:
    index = int(input("Index: "))
    print(numbers[index])

except ValueError:
    print("error: correct integer numeric value of index should be entered")
except IndexError:
    print(f"error: index should be between {-len(numbers)} and {len(numbers)-1}")
