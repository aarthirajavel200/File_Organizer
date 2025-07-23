import streamlit as st
import os
import shutil
from PIL import Image

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

# Move a file to its target category folder
def move_file(file_path, base_path, folder_name):
    target_folder = os.path.join(base_path, folder_name)
    os.makedirs(target_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))

# Organize files inside the temp directory
def organize_uploaded_files(upload_folder, status_text):
    files_moved = {}
    all_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    total = len(all_files)

    progress_bar = st.progress(0)

    for i, filename in enumerate(all_files):
        file_path = os.path.join(upload_folder, filename)
        _, extension = os.path.splitext(filename)
        moved = False

        for category, extensions in FILE_CATEGORIES.items():
            if extension.lower() in extensions:
                move_file(file_path, upload_folder, category)
                files_moved.setdefault(category, []).append(filename)
                moved = True
                break

        if not moved:
            move_file(file_path, upload_folder, "Others")
            files_moved.setdefault("Others", []).append(filename)

        # Progress
        status_text.text(f"Organizing: {filename} ({i+1}/{total})")
        progress_bar.progress((i + 1) / total)

    return files_moved

# Streamlit UI
st.title("Simple File Organizer (Uploaded Files)")

uploaded_files = st.file_uploader("Upload multiple files to organize", accept_multiple_files=True)

if uploaded_files:
    working_dir = "temp_upload"
    os.makedirs(working_dir, exist_ok=True)

    # Save all uploaded files
    for uploaded_file in uploaded_files:
        with open(os.path.join(working_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

    if st.button("Organize Uploaded Files"):
        status_text = st.empty()
        status_text.info("Organizing files, please wait...")

        result = organize_uploaded_files(working_dir, status_text)

        status_text.success("Files organized successfully.")
        st.balloons()

        if result:
            st.subheader("Summary of Files Organized:")
            for category, files in result.items():
                st.write(f"{category}: {len(files)} file(s)")
                for file in files:
                    st.markdown(f"- {file}")
        else:
            st.write("No files were organized.")
