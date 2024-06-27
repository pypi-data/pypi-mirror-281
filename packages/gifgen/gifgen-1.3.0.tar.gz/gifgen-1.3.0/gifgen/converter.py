from PIL import Image
import os

def convert_images_to_gif(image_folder_paths, output_folder, duration=500):
    """
    Convert images in given folders to GIFs.
    
    :param image_folder_paths: List of paths to folders containing images or a single path.
    :param output_folder: Path to folder where GIFs will be saved.
    :param duration: Duration for each frame in the GIF.
    """
    # If a single folder path is provided, convert it to a list
    if isinstance(image_folder_paths, str):
        image_folder_paths = [image_folder_paths]
    
    for folder_path in image_folder_paths:
        if os.path.isdir(folder_path):
            # Check if the folder path has subfolders
            subfolders = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
            if not subfolders:
                subfolders = [folder_path]

            for subfolder in subfolders:
                images = []
                for file_name in sorted(os.listdir(subfolder)):
                    if file_name.endswith('.png') or file_name.endswith('.jpeg') or file_name.endswith('.jpg'):
                        image_path = os.path.join(subfolder, file_name)
                        images.append(Image.open(image_path))

                if images:
                    gif_path = os.path.join(output_folder, os.path.basename(subfolder) + '.gif')
                    images[0].save(
                        gif_path,
                        save_all=True,
                        append_images=images[1:],
                        duration=duration,
                        loop=0
                    )
                    print(f'Successfully created GIF: {gif_path}')
                else:
                    print(f'No images found in folder: {subfolder}')
        else:
            print(f'Invalid folder path: {folder_path}')
