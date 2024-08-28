import re

def insert_page_breaks_and_special_phrases(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    page_break = "\\newpage\n"
    chapter_pattern = re.compile(r"第.*回")

    output_lines = []

    first_chapter = True
    chapter_counter = 1  # 用于生成唯一的书签标签

    for line in lines:
        if chapter_pattern.search(line):
            if not first_chapter:
                output_lines.append(page_break)  # Insert page break before chapter title
            else:
                first_chapter = False  # Skip page break before the first chapter

            chapter_title = line.rstrip()
            bookmark_label = f"chapter{chapter_counter}"
            output_lines.append("\\pdfbookmark[1]{" + chapter_title + "}{" + bookmark_label + "}\n")  # Add bookmark with title and label
            output_lines.append("\\chapter*{\\centering \\normalsize \\textbf{" + chapter_title + "}}\n")  # Center and bold chapter title in normal size
            output_lines.append("\\addcontentsline{toc}{chapter}{" + chapter_title + "}\n")  # Ensure title is added to TOC
            chapter_counter += 1
        else:
            output_lines.append("\\noindent \\hspace*{2em}" + line.rstrip() + " \\\\\n")  # Add LaTeX line break to each line with space
            
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)
    
    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-1', '-3')
insert_page_breaks_and_special_phrases(input_file, output_file)

