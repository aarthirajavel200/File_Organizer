import streamlit as st
import zipfile
import os
import shutil
import tempfile
from pathlib import Path

# Define file categories
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

def move_file(file_path, base_path, folder_name):
    target_folder = os.path.join(base_path, folder_name)
    os.makedirs(target_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))

def organize_folder(folder_path, status_text):
    files_moved = {}
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total = len(all_files)

    progress_bar = st.progress(0)

    for i, filename in enumerate(all_files):
        file_path = os.path.join(folder_path, filename)
        _, extension = os.path.splitext(filename)
        moved = False

        for category, extensions in FILE_CATEGORIES.items():
            if extension.lower() in extensions:
                move_file(file_path, folder_path, category)
                files_moved.setdefault(category, []).append(filename)
                moved = True
                break

        if not moved:
            move_file(file_path, folder_path, "Others")
            files_moved.setdefault("Others", []).append(filename)

        status_text.text(f"Organizing: {filename} ({i+1}/{total})")
        progress_bar.progress((i + 1) / total)

    return files_moved

# Streamlit App
st.set_page_config(page_title="File Organizer", page_icon="🗂️")
st.title("📂 Simple File Organizer with Categories")

uploaded_zip = st.file_uploader("Upload a ZIP file containing files to organize", type=["zip"])

if uploaded_zip is not None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.getbuffer())

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)

        status_text = st.empty()
        status_text.info("Processing started. Please wait...")

        result = organize_folder(tmp_dir, status_text)

        status_text.success("Files organized successfully.")
        st.balloons()

        # Zip organized folder
        organized_zip_path = os.path.join(tmp_dir, "organized_files.zip")
        with zipfile.ZipFile(organized_zip_path, "w") as zf:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    if file != "uploaded.zip" and file != "organized_files.zip":
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, tmp_dir)
                        zf.write(file_path, arcname)

        st.download_button(
            label="📥 Download Organized Files as ZIP",
            data=open(organized_zip_path, "rb"),
            file_name="organized_files.zip",
            mime="application/zip"
        )

        if result:
            st.subheader("📊 Summary of Files Moved:")
            for category, files in result.items():
                st.write(f"**{category}**: {len(files)} file(s)")
                for file in files:
                    st.markdown(f"- {file}")
        else:
            st.write("No files were moved.")
