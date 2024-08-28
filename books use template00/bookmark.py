import fitz  # PyMuPDF
import os

def extract_text_from_page(pdf_document, page_number):
    page = pdf_document.load_page(page_number)
    text = page.get_text("text")
    return text

def find_bookmarks(pdf_document):
    bookmarks = []
    for page_number in range(len(pdf_document)):
        text = extract_text_from_page(pdf_document, page_number)
        lines = text.split('\n')
        for line in lines:
            if "第" in line and "回" in line:
                bookmarks.append({"title": line.strip(), "page": page_number + 1})
    return bookmarks

def add_bookmarks(input_file):
    # 打开现有的 PDF 文件
    pdf_document = fitz.open(input_file)
    
    # 查找书签
    bookmarks = find_bookmarks(pdf_document)
    
    # 遍历书签列表，添加书签
    for bookmark in bookmarks:
        title = bookmark["title"]
        page_number = bookmark["page"]
        # 添加书签到指定页码，位置（x, y）可以根据需要调整
        pdf_document.add_outline(page_number - 1, title, fitz.Point(72, 72))
    
    # 生成输出文件名
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}002{ext}"
    
    # 保存修改后的 PDF 文件
    pdf_document.save(output_file)
    
    print(f"书签已添加并保存为 '{output_file}'")

# 输入文件名
input_file = "input.pdf"  # 替换为你的输入文件名
add_bookmarks(input_file)
