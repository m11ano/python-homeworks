check = set()

with open(file='./input.txt', mode='r', encoding='utf-8') as source_file:
    with open(file='./unique_output.txt', mode='w', encoding='utf-8') as destination_file:
        for line in source_file:
            if line not in check:
                destination_file.write(line)
                check.add(line)

print("Done")