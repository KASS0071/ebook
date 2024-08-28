import PyPDF2

def is_blank_page(page):
    """Determine if a page is blank by checking text content."""
    text = page.extract_text()
    return not text.strip()

def remove_blank_pages(input_pdf, output_pdf):
    with open(input_pdf, 'rb') as infile, open(output_pdf, 'wb') as outfile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            if not is_blank_page(page):
                writer.add_page(page)

        writer.write(outfile)
        print(f"Blank pages removed. Output saved to {output_pdf}")

if __name__ == "__main__":
    input_pdf = input("Enter the path to the input PDF (with blank pages): ")
    output_pdf = input("Enter the path to the output PDF (without blank pages): ")
    remove_blank_pages(input_pdf, output_pdf)
