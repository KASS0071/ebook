import re

def process_text(input_filename, output_filename):
    # 打开并读取输入文件
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    paragraphs = []  # 用于存储段落
    current_paragraph = []  # 当前段落的内容

    # 遍历文件中的每一行
    for line in lines:
        stripped_line = line.strip()  # 去除行首尾的空白字符
        if stripped_line:  # 如果行非空
            current_paragraph.append(stripped_line)
        else:  # 如果遇到空行，表示一个段落的结束
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))  # 将句子合并成段落
                current_paragraph = []  # 清空当前段落

    if current_paragraph:  # 如果最后还有未处理的段落
        paragraphs.append(" ".join(current_paragraph))

    # 将处理后的段落写入输出文件
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(paragraphs))

    # 打印提示信息
    print(f"处理后的文本已保存至 '{output_filename}'")

# 用户输入文件名
input_filename = input("请输入输入文本文件名（包括路径）：")
output_filename = input("请输入输出文本文件名（包括路径）：")

# 处理文本文件
process_text(input_filename, output_filename)

