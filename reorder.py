import sys
import time
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]

# Function to impose pages for saddle-stitching
def reorder(input_pdf, output_pdf):
    reader = PyPDF2.PdfReader(input_pdf)
    num_pages = len(reader.pages)
    
    # Ensure the number of pages is a multiple of 4
    if num_pages % 4 != 0:
        print("Please provide a PDF file with page count that is a multiple of 4.")
        time.sleep(5)
        sys.exit(1)

    saddle_order = flat_map(lambda i: [i + 1,num_pages - i] if i%2!=0 else [num_pages - i,i + 1], range(num_pages // 2))
    print("saddle_order",saddle_order)

    impose_order = flat_map(lambda i: saddle_order[-4*(i+1):-4*i] if i>0 else saddle_order[-4:], range(len(saddle_order)//4))
    print("impose_order",impose_order)

    # Create a new PDF for the imposed pages
    writer = PyPDF2.PdfWriter()
    for page_num in impose_order:
            page = reader.pages[page_num - 1]
            writer.add_page(page)
    
    with open(output_pdf, "wb") as f_out:
        writer.write(f_out)

if __name__ == "__main__":
    # Check if the user provided a file path
    if len(sys.argv) < 2:
        print("Please provide the path to a PDF file.")
        time.sleep(5)
        sys.exit(1)

    # Take the first argument as the input file
    input_pdf_path = sys.argv[1]
    output_pdf_path = input_pdf_path[:-4] + " (re-ordered pages).pdf"

    # Call the reorder function
    reorder(input_pdf_path, output_pdf_path)

