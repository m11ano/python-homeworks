try:
    import math

    num = float(input("Num: "))

    try:
        result = math.sqrt(num)
    except ValueError:
        print("error: can't take the square root of a negative number")
    else:
        print(result)

except ImportError:
    print("error: cant import math module")
except ValueError:
    print("error: correct float numeric value should be entered")

