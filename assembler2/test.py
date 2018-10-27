line = "    helloo #test"
print(line)
if '#' in line:
    line = line[0:line.find('#')]
    line = line.strip()

print(line)
