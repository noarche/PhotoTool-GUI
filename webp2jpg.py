import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def convert_webp_to_jpg(file_path):
    try:
        # Open the webp image
        img = Image.open(file_path)
        
        # Save as jpg
        jpg_path = os.path.splitext(file_path)[0] + ".jpg"
        img.convert("RGB").save(jpg_path, "JPEG")
        
        # Close the image
        img.close()
        
        # Delete the original webp file
        os.remove(file_path)
        
        print(f"Conversion successful: {file_path} -> {jpg_path}")
    except Exception as e:
        print(f"Error converting {file_path}: {e}")

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    directory = filedialog.askdirectory(title="Select Directory with WebP Images")
    if directory:
        convert_images_in_directory(directory)

def convert_images_in_directory(directory):
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".webp"):
            file_path = os.path.join(directory, filename)
            convert_webp_to_jpg(file_path)

def main():
    select_directory()

if __name__ == "__main__":
    main()
