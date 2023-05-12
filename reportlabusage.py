from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Create a new PDF file
pdf_file = 'document.pdf'
doc = SimpleDocTemplate(pdf_file, pagesize=letter)

# Define the text to be added to the PDF
text = 'Hello, World!\n' * 50

# Define the styles to use in the PDF
styles = getSampleStyleSheet()
style = styles['Normal']

# Define the list of paragraphs to add to the PDF
paragraphs = []
for line in text.split('\n'):
    paragraph = Paragraph(line, style)
    paragraphs.append(paragraph)
    paragraphs.append(Spacer(1, 0.2 * inch))

# Add the list of paragraphs to the PDF
doc.build(paragraphs)
