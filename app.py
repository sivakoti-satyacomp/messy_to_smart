from engine import *

import streamlit as st


# Initializes Streamlit session variables (logs and duplicates) if they do not already exist.
def initialize_session_state():
    
    if "logs" not in st.session_state:
        st.session_state.logs=[]

    if "duplicates" not in st.session_state:
        st.session_state.duplicates=[]



#Creates the sidebar UI components such as folder path input and action buttons, and returns user selections.
def show_sidebar():
    st.sidebar.header("⚙️ Settings")
    folder_path=st.sidebar.text_input("Enter messy folder path")

    #Create buton
    organize_btn=st.sidebar.button("📁 Organise files")
    duplicates_btn=st.sidebar.button("🔦 Find duplicates")
    clear_btn=st.sidebar.button("🗑️ Clear logs")

    return (folder_path,organize_btn,duplicates_btn,clear_btn)


#Validates the folder path, invokes the file organization process, updates logs, and displays the result to the user.
def handle_organize(folder_path):
    
    if not os.path.exists(folder_path):
        st.error("🛑 Invalid folder path")
        return
    
    #when valid
    logs=organize_files(folder_path)
    st.session_state.logs.extend(logs)

    st.success(" ℹ️ Successfully organized")


# Validates the folder path, scans for duplicate files, and stores the results in the session state.
def handle_find_duplicates(folder_path):
    
    if not os.path.exists(folder_path):
        st.error("🛑 Invalid folder path")
        return

    duplicates=find_duplicates(folder_path)
    st.session_state.duplicates.extend(duplicates)

# Displays detected duplicate files and provides an option to move them into the Duplicates folder.
def display_duplicates(folder_path):
    print("Hello")
    if not st.session_state.duplicates:
        return

    st.warning(f"⛔️ Found {len(st.session_state.duplicates)}!")    
    st.subheader("Duplicates below")

    for file in st.session_state.duplicates:
        st.write(file)

    if st.button("➡️ Move duplicates"):
        logs=move_duplicates(folder_path,st.session_state.duplicates)

        st.session_state.logs.extend(logs)

        st.success(" ℹ️ Successfully duplicates moves")

        st.session_state.duplicates=[] #reset my session variables


#Displays the latest activity logs generated during file organization and duplicate handling.
def display_logs():
    st.subheader("🪵 Activity logs")
    for msg in st.session_state.logs:
        st.write(msg)

# Acts as the controller of the application by coordinating all UI components and function calls.
initialize_session_state()
folder_path,organise_btn, duplicates_btn, clear_logs=show_sidebar()

if duplicates_btn:
    handle_find_duplicates(folder_path)

if organise_btn:
    handle_organize(folder_path)


display_duplicates(folder_path)
display_logs()

