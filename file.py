import streamlit as st
import os
import re

# -------- Helper Functions -------- #

def sanitize_filename(name):
    """Remove unsafe characters from filename."""
    return re.sub(r'[^a-zA-Z0-9_\-.]', '_', name)

def create_file(file_path):
    """Create a new text file with initial content."""
    try:
        with open(file_path, 'w') as file:
            file.write("This is the initial content of the file.\n")
        st.success(f"File created successfully at: {file_path}")
    except Exception as e:
        st.error(f"Error creating file: {e}")

def delete_file(file_path):
    """Delete the specified file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success(f"File deleted: {file_path}")
        else:
            st.warning("File does not exist.")
    except Exception as e:
        st.error(f"Error deleting file: {e}")

def list_files_in_directory(directory):
    """List all files in the specified directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        st.error(f"Error accessing directory: {e}")
        return []

def show_file_content(file_path):
    """Show content of the selected file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        st.text_area("File Content", content, height=200)
    except Exception as e:
        st.error(f"Unable to read file: {e}")

# -------- Streamlit UI -------- #

st.set_page_config(page_title="File Manager App", layout='centered')
st.title("📁 File Manager with Path Selection")

st.write("Create, delete, or view files by entering a custom path.")

operation = st.selectbox("Choose an operation:", ["Create File", "Delete File", "View File"])

directory = st.text_input("Enter the directory path:", value=os.getcwd())

if not os.path.isdir(directory):
    st.warning("Please enter a valid directory path.")
else:
    if operation == "Create File":
        file_name = st.text_input("Enter new file name (e.g., `note.txt`):")
        if st.button("Create File"):
            if file_name.strip():
                safe_name = sanitize_filename(file_name.strip())
                full_path = os.path.join(directory, safe_name)
                if not os.path.exists(full_path):
                    create_file(full_path)
                else:
                    st.warning("File already exists.")
            else:
                st.warning("Please enter a valid file name.")

    elif operation == "Delete File":
        files = list_files_in_directory(directory)
        if files:
            file_to_delete = st.selectbox("Select file to delete:", files)
            if st.button("Delete File"):
                delete_file(os.path.join(directory, file_to_delete))
        else:
            st.info("No files found to delete in the selected directory.")

    elif operation == "View File":
        files = list_files_in_directory(directory)
        if files:
            file_to_view = st.selectbox("Select file to view:", files)
            show_file_content(os.path.join(directory, file_to_view))
        else:
            st.info("No files available to view in the selected directory.")

    # Optional: List all files in the selected directory
    st.markdown("---")
    st.subheader("📄 Files in Selected Directory:")
    st.code("\n".join(list_files_in_directory(directory)) or "No files found.")
