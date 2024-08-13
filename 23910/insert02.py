import re

def insert_page_breaks_and_newlines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    first_chapter_pattern = re.compile(r"第一回")
    chapter_pattern = re.compile(r"第.*回")
    end_of_chapter_phrase = "下回分解。"

    output_lines = []
    is_first_chapter = True

    for line in lines:
        if is_first_chapter and first_chapter_pattern.search(line):
            output_lines.append("\\newpage\n")  # Insert page break before "第一回"
            is_first_chapter = False

        if chapter_pattern.search(line):
            output_lines.append("\\noindent \\textbf{" + line.rstrip() + "} \\\\\n")  # Bold chapter title
            output_lines.append("\n")  # Add an extra blank line after the chapter title
        else:
            # Insert newline after specific phrase within the same line
            modified_line = line.replace(end_of_chapter_phrase, end_of_chapter_phrase + "\n")
            output_lines.append("\\noindent \\hspace*{2em}" + modified_line.rstrip() + " \\\\\n")  # Add LaTeX line break to each line with space

            # Add new page after "下回分解。"
            if end_of_chapter_phrase in line:
                output_lines.append("\\newpage\n")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)
    
    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-3', '-1')
insert_page_breaks_and_newlines(input_file, output_file)

