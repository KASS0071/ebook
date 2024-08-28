import re

def insert_page_breaks_and_newlines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chapter_pattern = re.compile(r"第.*回")

    output_lines = []

    for line in lines:
        if chapter_pattern.search(line):
            output_lines.append("\\newpage\n")  # Insert page break before each chapter
            output_lines.append("\\centerline{\\textbf{" + line.rstrip() + "}} \n")  # Center and bold chapter title
            output_lines.append("\n")  # Add an extra blank line after the chapter title
        else:
            # Add a LaTeX line break to each line with space
            output_lines.append("\\noindent \\hspace*{2em}" + line.rstrip() + " \\\\\n")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)
    
    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-2', '-3')
insert_page_breaks_and_newlines(input_file, output_file)


