import re

def add_newline_after_phrase(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Define the phrase and the pattern to find it
    phrase = "下回分解。"
    pattern = re.compile(r'下回分解。')

    # Replace the phrase with the phrase followed by a newline
    modified_text = pattern.sub(phrase + '\n', text)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(modified_text)
    
    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-0', '-3')
add_newline_after_phrase(input_file, output_file)

