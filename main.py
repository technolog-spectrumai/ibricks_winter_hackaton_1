import streamlit as st
from PyPDF2 import PdfReader
import requests

st.title("📄 PDF Uploader App with Pinata")

# Create a form for entering Pinata JWT
with st.form("pinata_form"):
    pinata_jwt = st.text_input("Enter your Pinata JWT", type="password")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    submit_button = st.form_submit_button("Upload to Pinata")

if submit_button and uploaded_file is not None and pinata_jwt:
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

    # Upload to Pinata
    st.subheader("Uploading to IPFS…")
    try:
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {
            "Authorization": f"Bearer {pinata_jwt}"
        }
        files = {
            "file": (uploaded_file.name, uploaded_file, "application/pdf")
        }

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            cid = response.json()["IpfsHash"]

            # Green success box with border and bold CID
            st.markdown(
                f"""
                        <div style="border:2px solid green; padding:15px; border-radius:10px; background-color:#e6ffe6;">
                            <h2 style="color:green;">✅ File successfully uploaded to IPFS</h2>
                            <h1 style="color:green;"><b>CID: {cid}</b></h1>
                        </div>
                        """,
                unsafe_allow_html=True
            )
        else:
            st.error(f"Failed to upload: {response.text}")

    except Exception as e:
        st.error(f"Error uploading to IPFS: {e}")
elif submit_button and not pinata_jwt:
    st.error("Please enter your Pinata JWT before uploading.")

