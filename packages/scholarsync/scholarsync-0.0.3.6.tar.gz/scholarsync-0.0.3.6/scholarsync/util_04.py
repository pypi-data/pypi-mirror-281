import os
import shutil

def sort_files_by_extension(directory):
    # Get the extension from user input
    extension = input("Enter the file extension (without the '.' character): ")

    # Create a directory to store the sorted files
    # Using os.getcwd() to get the current working directory
    sorted_directory = os.path.join(os.getcwd(), extension)
    os.makedirs(sorted_directory, exist_ok=True)

    # Traverse the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            # Check if the file has the desired extension
            if file.endswith('.' + extension):
                # Construct the destination file path
                dest_file_path = os.path.join(sorted_directory, file)

                # If the file already exists, add a number to the filename
                if os.path.exists(dest_file_path):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    new_file_name = f"{base}_{counter}{ext}"
                    dest_file_path = os.path.join(sorted_directory, new_file_name)

                    while os.path.exists(dest_file_path):
                        counter += 1
                        new_file_name = f"{base}_{counter}{ext}"
                        dest_file_path = os.path.join(sorted_directory, new_file_name)

                # Copy the file to the sorted directory with the unique name
                shutil.copy(file_path, dest_file_path)

    print(f"All files with extension '{extension}' have been copied to '{sorted_directory}'.")


def file_sorter():
    print("This generates a flat file sytem of a purticular extention by crawling into subdirectory tree")
    print("This is mainly used to collect the fragmented files of an extention, deduplicator can also be run after this")
    # Get the directory path from user input
    directory_path = input("Enter the directory path: ")
    sort_files_by_extension(directory_path)

if __name__ == "__main__":
    file_sorter()

