import fitz  # PyMuPDF
import os
import re
from pypdf import PdfReader, PdfWriter

# 汉字数字对应的数字映射表
chinese_numbers = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '十': 10
}

def chinese_to_number(chinese):
    if chinese in chinese_numbers:
        return chinese_numbers[chinese]
    if '十' in chinese:
        parts = chinese.split('十')
        if len(parts) == 2:
            if parts[0] == '':
                return 10 + chinese_numbers.get(parts[1], 0)
            elif parts[1] == '':
                return chinese_numbers.get(parts[0], 0) * 10
            else:
                return chinese_numbers.get(parts[0], 0) * 10 + chinese_numbers.get(parts[1], 0)
    return -1

def extract_text_from_page(pdf_document, page_number):
    page = pdf_document.load_page(page_number)
    text = page.get_text("text")
    return text

def find_bookmarks(pdf_document):
    bookmarks = []
    pattern = re.compile(r"第([零一二三四五六七八九十]+)回")
    for page_number in range(len(pdf_document)):
        text = extract_text_from_page(pdf_document, page_number)
        lines = text.split('\n')
        for line in lines:
            match = pattern.search(line)
            if match:
                chapter_number_chinese = match.group(1)
                chapter_number = chinese_to_number(chapter_number_chinese)
                if chapter_number != -1:
                    bookmarks.append({"title": line.strip(), "page": page_number, "chapter": chapter_number})
    return bookmarks

def filter_and_sort_bookmarks(bookmarks):
    # 按章节号排序
    bookmarks = sorted(bookmarks, key=lambda x: x["chapter"])
    
    # 过滤掉不连续的章节
    filtered_bookmarks = []
    expected_chapter = 1
    for bookmark in bookmarks:
        if bookmark["chapter"] == expected_chapter:
            filtered_bookmarks.append(bookmark)
            expected_chapter += 1
    return filtered_bookmarks

def generate_output_filename(input_filename):
    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}002{ext}"
    return output_filename

def add_bookmarks_to_pdf(input_filename):
    # 打开现有的 PDF 文件
    pdf_document = fitz.open(input_filename)

    # 查找书签
    bookmarks = find_bookmarks(pdf_document)

    # 过滤和排序书签
    filtered_bookmarks = filter_and_sort_bookmarks(bookmarks)

    # 生成输出文件名
    output_filename = generate_output_filename(input_filename)

    # 使用 pypdf 创建新的 PDF 并添加书签
    reader = PdfReader(input_filename)
    writer = PdfWriter()

    # 复制所有页面到新的 PDF
    for page in reader.pages:
        writer.add_page(page)

    # 添加书签
    for bookmark in filtered_bookmarks:
        title = bookmark["title"]
        page_number = bookmark["page"]
        writer.add_outline_item(title, page_number)

    # 写入新的 PDF 文件
    with open(output_filename, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"书签已添加并保存为 '{output_filename}'")

# 用户输入文件名
input_filename = input("请输入 PDF 文件名（包括路径）：")

# 添加书签到 PDF 文件
add_bookmarks_to_pdf(input_filename)

