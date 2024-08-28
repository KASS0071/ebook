import re

def insert_page_breaks_and_preserve_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    page_break = "\\newpage\n"
    chapter_pattern = re.compile(r"第.*回")
    output_lines = []

    for line in lines:
        if chapter_pattern.search(line):
            output_lines.append(page_break)  # Insert page break before chapter title
            output_lines.append(line.rstrip() + " \\\\\n")  # Add the chapter title with LaTeX line break
            output_lines.append("\n")  # Add an extra blank line after the chapter title
        else:
            output_lines.append(line.rstrip() + " \\\\\n")  # Add LaTeX line break to each line

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

input_file = '57278-0.txt'
output_file = '57278-2.txt'
insert_page_breaks_and_preserve_lines(input_file, output_file)
