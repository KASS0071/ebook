# Read the contents of the file
with open('57278-2.txt', 'r') as file:
    data = file.read()

# Replace all occurrences of '???'
data = data.replace('???', '')

# Write the modified contents back to the file
with open('filename.txt', 'w') as file:
    file.write(data)

