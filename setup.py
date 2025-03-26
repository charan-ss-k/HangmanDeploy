import os
import shutil

# Create api/static/images directory if it doesn't exist
api_images_dir = os.path.join('api', 'static', 'images')
os.makedirs(api_images_dir, exist_ok=True)

# Move image files from static/images to api/static/images
source_dir = os.path.join('static', 'images')
for i in range(7):  # 0 through 6
    source_file = os.path.join(source_dir, f'hangman-{i}.png')
    dest_file = os.path.join(api_images_dir, f'hangman-{i}.png')
    if os.path.exists(source_file):
        shutil.copy2(source_file, dest_file)
        print(f'Moved {source_file} to {dest_file}')