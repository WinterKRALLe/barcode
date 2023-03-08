import cv2
import os
import argparse
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
from PyPDF3 import PdfFileWriter, PdfFileReader


def Extract_Code_From_PDF(input_file, output_file, code_type):
    
    output = PdfFileWriter()
    input1 = PdfFileReader(open(input_file, "rb"))

    output_page = input1.getPage(0)

    #bar code
    if 'bar' in code_type.lower():
        output_page.cropBox.lowerLeft = (0, 0)
        output_page.cropBox.upperleft = (0, 100)
        output_page.cropBox.lowerRight = (286, 0)
        output_page.cropBox.upperRight = (286, 100)


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


    pages = convert_from_path(output_file, dpi=300, first_page=0, last_page=0)
    image = pages[0]


    image_path = f"{pdf_dir}/page.png"

    image.save(image_path)

    image = cv2.imread(image_path)


    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    barcodes = decode(gray_image)


    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        bar = barcode.data.decode("utf-8")
        print("Barcode data:", barcode.data.decode("utf-8"))
        print("Barcode type:", barcode.type)

    new_file_path = os.path.join(os.path.expanduser(pdf_dir), bar)
    os.rename(input_file, new_file_path)

    os.remove(image_path)
    os.remove(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_dir', type=str, required=True,
                        help='Directory path containing PDF files.')
    args = parser.parse_args()

    pdf_dir = args.pdf_dir

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            file = os.path.join(pdf_dir, filename)
            print(file)
            rename(file)
