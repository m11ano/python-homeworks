with open(file='./source.txt', mode='r', encoding='utf-8') as source_file:
    with open(file='./destination.txt', mode='w', encoding='utf-8') as destination_file:
        for line in source_file:
            destination_file.write(line)

print("Done")