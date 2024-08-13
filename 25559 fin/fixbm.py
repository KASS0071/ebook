from PyPDF2 import PdfReader, PdfWriter

def update_bookmark(pdf_path, bookmark_title, correct_page):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copy all pages to the new PDF
    for page_num in range(len(reader.pages)):
        writer.addPage(reader.getPage(page_num))

    # Get the outlines (bookmarks) from the PDF
    outlines = reader.getOutlines()

    # Traverse and update bookmarks
    def traverse_and_update_bookmarks(outlines, correct_page):
        for outline in outlines:
            title = outline.title
            page_number = reader.getDestinationPageNumber(outline) + 1
            if title == bookmark_title:
                print(f"Updating bookmark '{bookmark_title}' from page {page_number} to page {correct_page}")
                outline.page['/Page'] = correct_page - 1

            # Recursively process child outlines
            if isinstance(outline, list):
                traverse_and_update_bookmarks(outline, correct_page)

    traverse_and_update_bookmarks(outlines, correct_page)

    # Save the updated PDF
    output_file = pdf_path.replace('.pdf', '-updated.pdf')
    with open(output_file, 'wb') as out_pdf:
        writer.write(out_pdf)

    print(f"Bookmark updated and saved to '{output_file}'")

# Input PDF file name
pdf_file = input("Enter the PDF file name (e.g., '57278-0.pdf'): ")
update_bookmark(pdf_file, "后記", 130)



