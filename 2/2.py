import re

sum = 0
try:
    with open(file='./prices.txt', mode='r', encoding='utf-8') as source_file:
        n = 0
        for line in source_file:
            n += 1
            data = re.split(r'\s+', line.strip())
            try:
                count = int(data[1])
                price = int(data[2])
                sum += count * price
            except:
                print(f"Line {n} bad format")
except FileNotFoundError:
    print("file not found")

print("Sum:", sum)