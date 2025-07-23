import streamlit as st
import os
import shutil
from PIL import Image

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

# Move file to target category folder
def move_file(file_path, base_path, folder_name):
    target_folder = os.path.join(base_path, folder_name)
    os.makedirs(target_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))

# Organize the folder
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

        # Update progress and status
        status_text.text(f"Organizing: {filename} ({i+1}/{total})")
        progress_bar.progress((i + 1) / total)

    return files_moved

# Streamlit UI
st.title("Simple File Organizer")

folder_path = st.text_input("Enter the full folder path to organize:")

if st.button("Organize"):
    if os.path.exists(folder_path):
        status_text = st.empty()
        status_text.info("Processing started. Please wait...")

        result = organize_folder(folder_path, status_text)

        status_text.success("Folder organized successfully.")
        st.balloons()  # Visual celebration

        if result:
            st.subheader("Summary of Files Moved:")
            for category, files in result.items():
                st.write(f"{category}: {len(files)} file(s)")
                for file in files:
                    st.markdown(f"- {file}")
        else:
            st.write("No files were moved.")
    else:
        st.error("The path entered does not exist. Please provide a valid folder path.")

