import streamlit as st
from PyPDF2 import PdfReader

# Title of the app
st.title("📄 PDF Uploader App")

# File uploader widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Display file details
    st.write("Filename:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)
    st.write("File size:", uploaded_file.size, "bytes")

    # Read PDF content
    pdf_reader = PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)
    st.write(f"Number of pages: {num_pages}")

    # Show text from the first page
    first_page = pdf_reader.pages[0]
    text = first_page.extract_text()
    st.subheader("Text from first page:")
    st.write(text if text else "No extractable text found.")
