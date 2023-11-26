import os
from tkinter import Tk, Label, Button, Entry, filedialog, ttk
from PIL import Image

class ImageConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Converter")

        self.input_path_label = Label(master, text="Input Path:")
        self.input_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

        self.input_path_entry = Entry(master, width=40)
        self.input_path_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_input_button = Button(master, text="Browse", command=self.browse_input_path)
        self.browse_input_button.grid(row=0, column=2, pady=10)

        self.output_path_label = Label(master, text="Output Path:")
        self.output_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

        self.output_path_entry = Entry(master, width=40)
        self.output_path_entry.grid(row=1, column=1, padx=10, pady=10)

        self.browse_output_button = Button(master, text="Browse", command=self.browse_output_path)
        self.browse_output_button.grid(row=1, column=2, pady=10)

        self.compression_label = Label(master, text="Compression Percentage:")
        self.compression_label.grid(row=2, column=0, padx=10, pady=10, sticky="E")

        self.compression_entry = Entry(master, width=40)
        self.compression_entry.grid(row=2, column=1, padx=10, pady=10)

        self.resize_label = Label(master, text="Resize Percentage:")
        self.resize_label.grid(row=3, column=0, padx=10, pady=10, sticky="E")

        self.resize_entry = Entry(master, width=40)
        self.resize_entry.grid(row=3, column=1, padx=10, pady=10)

        self.progress_label = Label(master, text="")
        self.progress_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=10)

        self.convert_button = Button(master, text="Convert", command=self.convert_images)
        self.convert_button.grid(row=6, column=0, columnspan=3, pady=20)

    def browse_input_path(self):
        input_path = filedialog.askdirectory()
        self.input_path_entry.delete(0, 'end')
        self.input_path_entry.insert(0, input_path)

    def browse_output_path(self):
        output_path = filedialog.askdirectory()
        self.output_path_entry.delete(0, 'end')
        self.output_path_entry.insert(0, output_path)

    def convert_images(self):
        input_path = self.input_path_entry.get()
        output_path = self.output_path_entry.get()
        compression_percentage = int(self.compression_entry.get())
        resize_percentage = int(self.resize_entry.get())

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        file_list = [filename for filename in os.listdir(input_path) if filename.lower().endswith(('.jpg', '.webp'))]
        total_files = len(file_list)

        if total_files == 0:
            self.progress_label.config(text="No JPEG or WebP files found.")
            return

        self.progress_bar['maximum'] = total_files
        self.progress_bar['value'] = 0

        for index, filename in enumerate(file_list, start=1):
            input_file_path = os.path.join(input_path, filename)
            output_file_path = os.path.join(output_path, os.path.splitext(filename)[0] + ".webp")

            img = Image.open(input_file_path)

            # Resize the image
            original_size = img.size
            new_size = (int(original_size[0] * resize_percentage / 100), int(original_size[1] * resize_percentage / 100))
            img = img.resize(new_size)

            img.save(output_file_path, 'WEBP', quality=compression_percentage)

            self.progress_bar['value'] = index
            self.progress_label.config(text=f"Converting {index}/{total_files} files")

        self.progress_label.config(text="Conversion complete.")

if __name__ == "__main__":
    root = Tk()
    app = ImageConverterApp(root)
    root.mainloop()
