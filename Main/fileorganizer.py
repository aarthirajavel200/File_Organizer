
import streamlit as st
import os
import zipfile
import shutil
from collections import defaultdict
import tempfile

def organize_files(uploaded_files):
    # Create a temporary directory for organizing files
    with tempfile.TemporaryDirectory() as temp_dir:
        organized_dir = os.path.join(temp_dir, "organized")
        os.makedirs(organized_dir, exist_ok=True)

        # Save uploaded files temporarily
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

        # Organize by file type
        file_type_folders = defaultdict(list)
        for file_name in os.listdir(temp_dir):
            if file_name == "organized":
                continue
            ext = os.path.splitext(file_name)[1][1:].lower()
            ext_folder = os.path.join(organized_dir, ext if ext else "no_extension")
            os.makedirs(ext_folder, exist_ok=True)
            shutil.move(os.path.join(temp_dir, file_name), os.path.join(ext_folder, file_name))

        # Create a zip file
        zip_path = os.path.join(temp_dir, "organized_files.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for foldername, _, filenames in os.walk(organized_dir):
                for filename in filenames:
                    abs_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(abs_path, organized_dir)
                    zipf.write(abs_path, arcname)

        # Read zip for download
        with open(zip_path, "rb") as f:
            zip_bytes = f.read()

        return zip_bytes

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="File Organizer", page_icon="📁")
st.title("📁 File Organizer")

uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)

if uploaded_files:
    if st.button("Organize Files"):
        try:
            zip_bytes = organize_files(uploaded_files)
            st.balloons()
            st.success("Files organized and zipped successfully!")
            st.download_button(" Download Organized Files", zip_bytes, file_name="organized_files.zip", mime="application/zip")
        except Exception as e:
            st.error(f"An error occurred: {e}")
