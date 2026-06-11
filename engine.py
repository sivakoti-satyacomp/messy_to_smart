import os
import shutil
import hashlib


file_types={
    "Images":["jpg","jpeg","png"],
    "Docs":["pdf","txt","docx","doc"],
    "Videos":["mp4","mkv","wma"],
    "Archives":["tar","zip","rar"]
}

# Extracts and returns the file extension (e.g., jpg, pdf, txt) from a filename.
def get_extension(filename):
    return filename.split('.')[-1]


# Creates a folder if it does not already exist and returns its path.
def create_folder(folder_path, folder_name):
    new_folder=os.path.join(folder_path,folder_name)
    os.makedirs(new_folder,exist_ok=True) 
    return new_folder


# Determines the file category (Images, Documents, Videos, Archives, Others) based on the file extension.
def get_category(extension):
    for category,extensions in file_types.items():
        if extension in extensions:
            return category
    return "Others"

# Organizes files into appropriate folders based on their category and returns the count and activity logs.
def organize_files(folder_path):
    logs=[]

    for filename in os.listdir(folder_path):
        file_path=os.path.join(folder_path,filename)
        
        #If directory do nothing
        if os.path.isdir(file_path):
            continue

        
        #if file is encountered
        extension=get_extension(filename)
        category=get_category(extension)

        destination_folder=create_folder(folder_path,category)
        shutil.move(file_path,os.path.join(destination_folder,filename))
        
        logs.append(f"Moved {filename} to {category}") #log is updated
    
    return logs



# Generates an MD5 hash value for a file. Used to uniquely identify file contents.
def get_file_hash(file_path):
    hasher=hashlib.md5()
    with open(file_path,"rb") as fp:
        while chunk:=fp.read(4096):
            hasher.update(chunk)
    
    return hasher.hexdigest()




# Scans all files in the folder, compares their hash values, and identifies duplicate files.
def find_duplicates(folder_path):
    
    file_hashes={}
    duplicates=[]

    for root,dirs,files in os.walk(folder_path):

        for file in files: #process duplicates of files only
            file_path=os.path.join(root,file)
            file_hash=get_file_hash(file_path)

            #if duplicate is found
            if file_hash in file_hashes:
                duplicates.append(file_path) 
            else:
                file_hashes[file_hash]=file_path #finger print not exist just store it
    
    return duplicates


# Moves duplicate files into a separate Duplicates folder and returns the count and activity logs.
def move_duplicates(folder_path, duplicates):
    
    duplicate_folder=create_folder(folder_path,"Duplicates")
    logs=[]
    #Traverse list of duplicates
    for file_path in duplicates:
        shutil.move(file_path,os.path.join(duplicate_folder)) #move it
        logs.append(f"Duplicate found {file_path} and moved")
    
    return logs






#main function
# print(get_extension("test1.jpg"))

# print(get_extension("test1.iit.jpg"))

# print(get_extension("test1.iitm.bs.pdf"))


