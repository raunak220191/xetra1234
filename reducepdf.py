import PyPDF2

def reduce_pdf_size(input_path, output_path):
    pdf_writer = PyPDF2.PdfWriter()

    with open(input_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

input_pdf = 'input.pdf'
output_pdf = 'output.pdf'
reduce_pdf_size(input_pdf, output_pdf)
