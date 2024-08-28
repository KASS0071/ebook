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
            title = match.group(1)
            titles.append({"title": title, "line": line_num + 1})

    return titles

def find_title_in_pdf(pdf_document, title):
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        if title in text:
            return page_num
    return -1

def insert_bookmarks_to_pdf(pdf_path, titles):
    pdf_document = fitz.open(pdf_path)
    writer = PdfWriter()
    reader = PdfReader(pdf_path)

    for i in range(len(reader.pages)):
        writer.add_page(reader.pages[i])

    for title in titles:
        page_number = find_title_in_pdf(pdf_document, title["title"])
        if page_number != -1:
            writer.add_outline_item(title["title"], page_number)

    output_file = pdf_path.replace('.pdf', '-with-bookmarks.pdf')
    with open(output_file, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"书签已添加到 '{output_file}'")

def process_pdf(input_text_file, pdf_file):
    titles = extract_titles_from_text(input_text_file)
    insert_bookmarks_to_pdf(pdf_file, titles)

# 输入文件名
input_text_file = input("请输入包含标题的文本文件名（例如 '57278-0.txt'）：")
pdf_file = input("请输入PDF文件名（例如 '57278-0.pdf'）：")
process_pdf(input_text_file, pdf_file)

