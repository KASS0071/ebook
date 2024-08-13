import re

def insert_page_breaks_and_newlines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    volume_pattern = re.compile(r"第.*卷")
    
    #chapter_pattern = re.compile(r"第.*回")

    output_lines = []

    for line in lines:
        if volume_pattern.search(line):
            output_lines.append("\\newpage\n")  # Start a new page for each volume
            output_lines.append("\\vspace*{\\fill}\n")  # Vertically center the title
            output_lines.append("\\begin{center}\n")
            output_lines.append("\\Huge \\textbf{" + line.strip() + "}\n")  # Make the volume title large and bold
            output_lines.append("\\end{center}\n")
            output_lines.append("\\vspace*{\\fill}\n")
            output_lines.append("\\newpage\n")  # Ensure the following text starts on a new page
        
        
        #elif chapter_pattern.search(line):
            #output_lines.append("\\newpage\n")  # Start a new page for each chapter
            #output_lines.append("\\centerline{\\textbf{" + line.strip() + "}} \n")  # Center and bold chapter title
            #output_lines.append("\n")  # Add an extra blank line after the chapter title
        else:
            # Add a LaTeX line break to each line with space
            output_lines.append("\\noindent \\hspace*{2em}" + line.strip() + " \\\\\n")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)
    
    print(f"Output written to {output_file}")

# Input file name
input_file = input("Enter the input file name (e.g., '57278-0.txt'): ")
output_file = input_file.replace('-0', '-1')
insert_page_breaks_and_newlines(input_file, output_file)

