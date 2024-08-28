import re
import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter
import os

def extract_titles_from_text(input_file):
    title_pattern = re.compile(r"\\centerline{\\textbf{(.+?)}}")
    titles = []

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line_num, line in enumerate(lines):
        match = title_pattern.search(line.strip())
        if match:
            title = match.group(1).strip()
            titles.append({"title": title, "line": line_num + 1})

    return titles

def find_title_in_pdf(pdf_document, title, page_offset=0):
    normalized_title = re.sub(r'\s+', '', title)  # Remove all whitespace for matching
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        normalized_text = re.sub(r'\s+', '', text)  # Remove all whitespace for matching
        if normalized_title in normalized_text:
            return page_num + page_offset
    return -1

def insert_bookmarks_to_pdf(pdf_path, titles, page_offset=0):
    pdf_document = fitz.open(pdf_path)
    writer = PdfWriter()
    reader = PdfReader(pdf_path)

    for i in range(len(reader.pages)):
        writer.add_page(reader.pages[i])

    for title in titles:
        page_number = find_title_in_pdf(pdf_document, title["title"], page_offset)
        if page_number != -1:
            print(f"Adding bookmark for '{title['title']}' on page {page_number + 1}")
            writer.add_outline_item(title["title"], page_number)
        else:
            print(f"Warning: Title '{title['title']}' not found in PDF")

    output_file = pdf_path.replace('.pdf', '-with-bookmarks.pdf')
    with open(output_file, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"书签已添加到 '{output_file}'")

def process_pdf(input_text_file, pdf_file, page_offset=0):
    titles = extract_titles_from_text(input_text_file)
    for title in titles:
        print(f"Found title '{title['title']}' at line {title['line']}")
    insert_bookmarks_to_pdf(pdf_file, titles, page_offset)

# 输入文件名
input_text_file = input("请输入包含标题的文本文件名（例如 '57278-0.txt'）：")
pdf_file = input("请输入PDF文件名（例如 '57278-0.pdf'）：")
page_offset = int(input("请输入页面偏移量（例如 '0'）："))
process_pdf(input_text_file, pdf_file, page_offset)


