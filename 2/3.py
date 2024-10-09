import re

count = 0
try:
    with open(file='./text_file.txt', mode='r', encoding='utf-8') as source_file:
        for line in source_file:
            found = line.strip().split()
            for item in found:
                if  re.search(r'[a-zA-Zа-яА-Я0-9]', item):
                    count += 1
                    
except FileNotFoundError:
    print("file not found")

print("Count:", count)