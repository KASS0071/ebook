import re

def remove_line_breaks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Join lines into a single string
    text = ''.join(lines)

    # Replace multiple newlines with a placeholder
    text = re.sub(r'\n\n+', '__PARAGRAPH_BREAK__', text)

    # Remove single newlines
    text = re.sub(r'\n', ' ', text)

    # Restore paragraph breaks
    text = re.sub(r'__PARAGRAPH_BREAK__', '\n\n', text)

    # Optionally, remove leading and trailing whitespace
    text = text.strip()

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)
    
    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-0', '-processed')
remove_line_breaks(input_file, output_file)

