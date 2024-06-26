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
## Alternate installation
- git clone https://github.com/yourusername/gifgen.git
- cd gifgen
- python setup.py install

## Usage
```
from gifgen.converter import convert_images_to_gif

image_folders = ['path/to/folder1', 'path/to/folder2']
output_folder = 'path/to/output'
convert_images_to_gif(image_folders, output_folder)
```




