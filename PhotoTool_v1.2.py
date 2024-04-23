import os
from tkinter import Tk, Button, filedialog, messagebox, ttk, simpledialog
from PIL import Image
import piexif
import webptools

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        strip_metadata(folder_path)
        messagebox.showinfo("Success", "Processing completed!")

def strip_metadata(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith((".jpg", ".jpeg", ".webp")):
            if filename.endswith((".jpg", ".jpeg")):
                with open(filepath, 'rb') as f:
                    image = Image.open(f)
                    image_data = list(image.getdata())
                    image_without_exif = Image.new(image.mode, image.size)
                    image_without_exif.putdata(image_data)
                    image_without_exif.save(filepath, "JPEG")
            elif filename.endswith(".webp"):
                webptools.strip(filepath)

def resize_images():
    directory = filedialog.askdirectory()
    if directory:
        percentage = simpledialog.askfloat("Input", "Enter resize percentage (e.g., 50 for 50%):", parent=root)
        if percentage:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if filename.endswith((".jpg", ".jpeg", ".webp")):
                    with open(filepath, 'rb') as f:
                        image = Image.open(f)
                        new_size = (int(image.width * (percentage / 100)), int(image.height * (percentage / 100)))
                        resized_image = image.resize(new_size)
                        if filename.endswith((".jpg", ".jpeg")):
                            resized_image.save(filepath, "JPEG")
                        elif filename.endswith(".webp"):
                            resized_image.save(filepath, "WEBP")
            messagebox.showinfo("Success", f"Resized all photos to {percentage}% of their original size.")

def compress_images():
    directory = filedialog.askdirectory()
    if directory:
        compression_quality = simpledialog.askinteger("Input", "Enter compression number (100 is no compression):", parent=root, minvalue=1, maxvalue=100)
        if compression_quality:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if filename.endswith((".jpg", ".jpeg", ".webp")):
                    if filename.endswith((".jpg", ".jpeg")):
                        with open(filepath, 'rb') as f:
                            image = Image.open(f)
                            image.save(filepath, "JPEG", quality=compression_quality)
                    elif filename.endswith(".webp"):
                        webptools.cwebp(filepath, filepath, q=compression_quality)
            messagebox.showinfo("Success", f"Compressed all photos with quality {compression_quality}.")

def add_keywords_to_images():
    directory = filedialog.askdirectory()
    if directory:
        keywords_input = simpledialog.askstring("Input", "Enter keywords separated by commas:", parent=root)
        if keywords_input:
            keywords = keywords_input.encode("utf-16")
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if filename.endswith((".jpg", ".jpeg", ".webp")):
                    if filename.endswith((".jpg", ".jpeg")):
                        with open(filepath, 'rb') as f:
                            exif_dict = piexif.load(f.read())
                            exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords
                            exif_bytes = piexif.dump(exif_dict)
                            with Image.open(filepath) as img:
                                img.save(filepath, "JPEG", exif=exif_bytes)
                    elif filename.endswith(".webp"):
                        pass  # WebP format doesn't support EXIF metadata
            messagebox.showinfo("Success", "Keywords added to all photos!")

def add_specific_metadata():
    directory = filedialog.askdirectory()
    if directory:
        artist = simpledialog.askstring("Metadata Input", "Enter Artist Name:", parent=root)
        copyright = simpledialog.askstring("Metadata Input", "Enter Copyright Info:", parent=root)
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filename.endswith((".jpg", ".jpeg", ".webp")):
                if filename.endswith((".jpg", ".jpeg")):
                    with open(filepath, 'rb') as f:
                        exif_dict = piexif.load(f.read())
                        if artist:
                            exif_dict["0th"][piexif.ImageIFD.Artist] = artist
                        if copyright:
                            exif_dict["0th"][piexif.ImageIFD.Copyright] = copyright
                        exif_bytes = piexif.dump(exif_dict)
                        with Image.open(filepath) as img:
                            img.save(filepath, "JPEG", exif=exif_bytes)
                elif filename.endswith(".webp"):
                    pass  # WebP format doesn't support EXIF metadata
        messagebox.showinfo("Success", "Metadata added to all photos!")

root = Tk()
root.title("Photo Processor")
root.geometry("400x400")
root.resizable(0, 0)

root.configure(bg="#2e2e2e")
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", foreground="white", background="#555555", padding=10)

select_folder_button = ttk.Button(root, text="Delete All Metadata", command=select_folder)
select_folder_button.pack(pady=60)

resize_button = ttk.Button(root, text="Resize Images", command=resize_images)
resize_button.pack(pady=5)

compress_button = ttk.Button(root, text="Compress Images", command=compress_images)
compress_button.pack(pady=5)

add_keywords_button = ttk.Button(root, text="Add Keywords Metadata (seperate with ,)", command=add_keywords_to_images)
add_keywords_button.pack(pady=5)

metadata_button = ttk.Button(root, text="Add Artist & Copyright Metadata", command=add_specific_metadata)
metadata_button.pack(pady=5)

root.mainloop()
