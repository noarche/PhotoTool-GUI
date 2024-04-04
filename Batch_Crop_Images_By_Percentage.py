import os
from PIL import Image

def crop_images(folder_path, percentage_to_remove):
    # Get list of files in folder
    files = os.listdir(folder_path)
    # Filter only image files (jpg or webp)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.webp'))]

    for filename in image_files:
        filepath = os.path.join(folder_path, filename)
        with Image.open(filepath) as img:
            # Calculate the cropping dimensions
            width, height = img.size
            crop_height = int(height * (percentage_to_remove / 100))
            box = (0, 0, width, height - crop_height)
            # Crop the image
            cropped_img = img.crop(box)
            # Save the cropped image
            cropped_img.save(filepath)

def main():
    folder_path = input("Enter the folder path containing images: ")
    percentage_to_remove = float(input("Enter the percentage of the bottom to remove (e.g., 10): "))

    crop_images(folder_path, percentage_to_remove)
    print("Images cropped successfully!")

if __name__ == "__main__":
    main()
