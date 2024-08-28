def add_indent_to_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    for line in lines:
        modified_line = "\\noindent \\hspace*{2em}" + line.rstrip() + " \\\\\n"
        output_lines.append(modified_line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-1', '-2')
add_indent_to_lines(input_file, output_file)

