import donut
import torch
from PIL import Image

# Load the pre-trained Donut model
model = donut.TransformerDonut()

# Load the document image
image_path = 'path_to_your_image.jpg'
image = Image.open(image_path)

# Preprocess the image for input to Donut
preprocessed_image = donut.TransformerDonut.preprocess(image)

# Perform document parsing using Donut
with torch.no_grad():
    output = model(preprocessed_image)

# Extract the relevant information from the output
document = output['document'][0]  # Assuming single-page document
text_lines = document['text_lines']
paragraphs = document['paragraphs']
tables = document['tables']
# ... extract other relevant information as needed

# Print the extracted text lines
print("Text Lines:")
for line in text_lines:
    print(line['text'])

# Print the extracted paragraphs
print("\nParagraphs:")
for paragraph in paragraphs:
    print(paragraph['text'])

# Print the extracted tables
print("\nTables:")
for table in tables:
    print(table['text'])
