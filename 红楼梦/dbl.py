def remove_blank_lines(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Remove blank lines
    non_blank_lines = [line for line in lines if line.strip()]
    
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.writelines(non_blank_lines)

    print(f"Blank lines removed and output saved to '{output_filename}'")

# 用户输入文件名
input_filename = input("请输入输入文本文件名（包括路径）：")
output_filename = input("请输入输出文本文件名（包括路径）：")

# 删除空行并保存新文件
remove_blank_lines(input_filename, output_filename)
