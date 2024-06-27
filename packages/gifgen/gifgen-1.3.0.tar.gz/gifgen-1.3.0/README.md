# gifgen

gifgen is a Python package for converting images in specified folders into GIFs. It provides a simple interface to create GIF animations from sets of images.

## Features

- Convert images in multiple folders into GIFs.
- Customize GIF duration per frame.
- Simple and easy-to-use interface.

## Installation

You can install gifgen using pip:

```bash
pip install gifgen
```

## Usage
    
    ```python
    from gifgen.converter import convert_images_to_gif

    # Example 1: Convert specific folders to GIFs with default duration (500 ms)
    image_folders = ['path/to/folder1', 'path/to/folder2']
    output_folder = 'path/to/output'
    convert_images_to_gif(image_folders, output_folder)

    # Example 2: Convert all subfolders of a parent folder to GIFs with custom duration (e.g., 500 ms)
    input_folder = 'input/*'
    output_folder = 'path/to/output'
    convert_images_to_gif(input_folder, output_folder, duration=500)
    ```
---