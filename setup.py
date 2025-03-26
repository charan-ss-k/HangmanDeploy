import os
import shutil

# Define the correct paths for Vercel deployment
api_images_dir = os.path.join('api', 'static', 'images')
static_images_dir = os.path.join('static', 'images')

# Create both image directories if they don't exist
os.makedirs(api_images_dir, exist=True)
os.makedirs(static_images_dir, exist=True)

# Copy hangman images to both locations to ensure they're available
for i in range(7):  # 0 through 6
    image_name = f'hangman-{i}.png'
    source_file = os.path.join(static_images_dir, image_name)
    dest_file_api = os.path.join(api_images_dir, image_name)
    
    # Copy from static to api if image exists
    if os.path.exists(source_file):
        shutil.copy2(source_file, dest_file_api)
        print(f'Copied {source_file} to {dest_file_api}')