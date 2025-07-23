import streamlit as st
import zipfile
import os
import shutil
import tempfile
from pathlib import Path

# File categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "PDF": [".pdf"],
    "Docx": [".docx"],
    "Powerpoint": [".pptx"],
    "Excel Files": [".xlsx", ".xls", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Python": [".py"],
    "Java": [".java"],
    "C": [".c"],
    "C++": [".cpp", ".cxx", ".cc"],
    "APKs": [".apk"],
    "JSON Files": [".json"],
    "Web Files": [".html", ".css", ".js", ".ts"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Others": []
}

def categorize_file(file_name):
    _, ext = os.path.splitext(file_name)
    for category, extensions in FILE_CATEGORIES.items():
        if ext.lower() in extensions:
            return category
    return "Others"

def organize_uploaded_zip(uploaded_zip):
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.getbuffer())

        # Extract uploaded zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        organized_dir = os.path.join(tmpdir, "organized")
        os.makedirs(organized_dir, exist_ok=True)

        files = [f for f in Path(tmpdir).rglob('*') if f.is_file() and f.name != "uploaded.zip"]

        progress_bar = st.progress(0)
        status = st.empty()

        for i, file_path in enumerate(files):
            category = categorize_file(file_path.name)
            target_folder = os.path.join(organized_dir, category)
            os.makedirs(target_folder, exist_ok=True)
            shutil.copy(file_path, os.path.join(target_folder, file_path.name))

            status.text(f"Organizing: {file_path.name} ({i+1}/{len(files)})")
            progress_bar.progress((i + 1) / len(files))

        # Create new organized zip
        final_zip_path = os.path.join(tmpdir, "organized_files.zip")
        with zipfile.ZipFile(final_zip_path, 'w') as zipf:
            for root, _, files in os.walk(organized_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, organized_dir)
                    zipf.write(full_path, arcname)

        st.success("Files organized successfully!")
        st.balloons()

        return final_zip_path

# Streamlit UI
st.title("📁 File Organizer into ZIP by File Type")
st.write("Upload a **.zip** file containing your unorganized files. This tool will categorize them and give you a new **organized .zip** file with subfolders for each type.")

uploaded_zip = st.file_uploader("Upload your zip folder here:", type=["zip"])

if uploaded_zip and st.button("Organize Files"):
    zip_result_path = organize_uploaded_zip(uploaded_zip)

    with open(zip_result_path, "rb") as f:
        st.download_button(
            label="📦 Download Organized ZIP",
            data=f,
            file_name="organized_files.zip",
            mime="application/zip"
        )

