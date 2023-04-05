import cv2
import os
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
from PyPDF3 import PdfFileWriter, PdfFileReader

pdf_dir = "/home/winter/Documents"
new_dir = "/home/winter/Pictures"

def Extract_Code_From_PDF(input_file, output_file, code_type):
    
    output = PdfFileWriter()
    input1 = PdfFileReader(open(input_file, "rb"))

    output_page = input1.getPage(0)

    #bar code
    if 'bar' in code_type.lower():
        x0 = 14.75 * 28.35  # Convert cm to points (1 cm = 28.35 points)
        y0 = (output_page.mediaBox.getHeight() - 26 * 28.35)
        x1 = 20.9 * 28.35
        y1 = (output_page.mediaBox.getHeight() - 28.66 * 28.35)

        output_page.mediaBox.lowerLeft = (x0, y0)
        output_page.mediaBox.lowerRight = (x1, y0)
        output_page.mediaBox.upperLeft = (x0, y1)
        output_page.mediaBox.upperRight = (x1, y1)

    #Data Matrix code
    # if 'matrix' in code_type.lower():
    #     output_page.cropBox.lowerLeft = (200, 309)
    #     output_page.cropBox.upperleft = (200, 378)
    #     output_page.cropBox.lowerRight = (270, 309)
    #     output_page.cropBox.upperRight = (270, 378)


    output.addPage(output_page)
    outputStream = open(output_file, "wb")
    output.write(outputStream)


def rename(input_file):

    output_file = rf"{pdf_dir}/outpyBar.pdf"

    # code_type = 'data matrix code'
    code_type = 'bar code'


    Extract_Code_From_PDF(input_file, output_file, code_type)


    pages = convert_from_path(input_file, first_page=0, last_page=0)
    image = pages[0]


    image_path = f"{pdf_dir}/page.png"

    image.save(image_path)

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    new = cv2.convertScaleAbs(image, alpha=1.2, beta=50)

    barcodes = decode(new)

    if not barcodes:
        print(f"No barcodes found in {input_file}")
        os.remove(image_path)
        os.remove(output_file)
        return

    print("Barcode data:", barcodes[0].data.decode("utf-8"))
    print("Barcode type:", barcodes[0].type)

    
    bar = barcodes[0].data.decode("utf-8")
    new_bar = bar.replace("/", "\\")
    new_file_path = os.path.join(os.path.expanduser(new_dir), f"{new_bar}.pdf")
    
    try:
        os.rename(input_file, new_file_path)
    except Exception as e:
        print(f"Error renaming file {input_file}: {e}")
        return

    os.remove(image_path)
    os.remove(output_file)


for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        file = os.path.join(pdf_dir, filename)
        print(file)
        rename(file)
