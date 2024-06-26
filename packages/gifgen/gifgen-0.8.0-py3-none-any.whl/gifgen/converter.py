# gifgen/converter.py
from PIL import Image
import os

def convert_images_to_gif(image_folder_paths, output_folder, duration=500):
    """
    Convert images in given folders to GIFs.
    
    :param image_folder_paths: List of paths to folders containing images.
    :param output_folder: Path to folder where GIFs will be saved.
    :param duration: Duration for each frame in the GIF.
    """
    for folder_path in image_folder_paths:
        images = []
        for file_name in sorted(os.listdir(folder_path)):
            if file_name.endswith('.png') or file_name.endswith('.jpeg') or file_name.endswith('.jpg'):
                image_path = os.path.join(folder_path, file_name)
                images.append(Image.open(image_path))

        if images:
            gif_path = os.path.join(output_folder, os.path.basename(folder_path) + '.gif')
            images[0].save(
                gif_path,
                save_all=True,
                append_images=images[1:],
                duration=duration,
                loop=0
            )
            print(f'Successfully created GIF: {gif_path}')
        else:
            print(f'No images found in folder: {folder_path}')
