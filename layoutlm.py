import streamlit as st
import requests
from PIL import Image
import torch
from transformers import LayoutLMForSequenceClassification, LayoutLMTokenizer

# Load the pre-trained model and tokenizer
model = LayoutLMForSequenceClassification.from_pretrained("microsoft/layoutlm-base-uncased")
tokenizer = LayoutLMTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")

# Define the FastAPI endpoint
def layout_lm_inference(question, image_path):
    # Read the image file
    image = Image.open(image_path)

    # Tokenize the question and image
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding="max_length", max_length=512)

    # Convert image to features
    image_features = tokenizer(images=image, return_tensors="pt", padding="max_length", max_length=512)

    # Update the input tensors
    inputs.update(image_features)

    # Perform inference
    outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits).item()

    return predicted_class

# Streamlit app
def main():
    st.title("Layout LM Question Answering")
    st.write("Upload an image and ask a question.")

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Text input for question
    question = st.text_input("Ask a question")

    # Check if image and question are provided
    if uploaded_file is not None and question:
        # Display the uploaded image
        st.image(uploaded_file, use_column_width=True)

        # Get the file path of the uploaded image
        image_path = f"uploaded_image.{uploaded_file.name.split('.')[-1]}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Perform layout LM inference
        result = layout_lm_inference(question, image_path)

        # Display the result
        st.write("Result:", result)

# Run the Streamlit app
if __name__ == "__main__":
    main()
