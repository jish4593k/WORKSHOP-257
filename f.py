from PyPDF2 import PdfFileReader, PdfFileWriter
import re


import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def create_toc(input_pdf, output_pdf, toc_file, page_offset):
    
    pdf_reader = PdfFileReader(open(input_pdf, 'rb'))
    pdf_writer = PdfFileWriter()

    
    for page_num in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page_num))


    with open(toc_file, 'r') as toc_lines:
        parents_bookmark = [None] * 10
        max_level = 10

        for line in toc_lines:
     
            tab_count = len(re.findall(r'^(\t*)', line)[0])

            if tab_count >= max_level:
                print('Too many levels in TOC.')
                return

            
            title = line.split(';')[0].lstrip('\t')
            page_number = int(line.split(';')[1].strip()) + page_offset
            parent = parents_bookmark[tab_count - 1] if tab_count > 0 else None

            pdf_writer.addBookmark(title, page_number, parent)
            parents_bookmark[tab_count] = pdf_writer.addBookmark(title, page_number, parent)

    # Save the new PDF with TOC
    with open(output_pdf, 'wb') as new_file:
        pdf_writer.write(new_file)

if __name__ == "__main__":
 
    input_pdf_file = 'InfoQ-2020中国技术发展白皮书.pdf'
    output_pdf_file = 'InfoQ-2020中国技术发展白皮书_toc.pdf'
    toc_file_name = 'toc-infoq.txt'
    page_offset_value = 3


    create_toc(input_pdf_file, output_pdf_file, toc_file_name, page_offset_value)


