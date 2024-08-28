import re

def process_text(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    paragraphs = []
    current_paragraph = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # if the line is not empty
            current_paragraph.append(stripped_line)
        else:  # if the line is empty, indicating a new paragraph
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []

    if current_paragraph:  # append the last paragraph if exists
        paragraphs.append(" ".join(current_paragraph))

    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(paragraphs))

    print(f"Processed text has been saved to '{output_filename}'")

# 用户输入文件名
input_filename = input("请输入输入文本文件名（包括路径）：")
output_filename = input("请输入输出文本文件名（包括路径）：")

# 处理文本文件
process_text(input_filename, output_filename)
