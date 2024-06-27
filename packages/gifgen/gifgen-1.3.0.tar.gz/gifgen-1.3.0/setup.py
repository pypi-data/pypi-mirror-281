# setup.py
from setuptools import setup, find_packages

setup(
    name='gifgen',
    version='1.3.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'gif-generator = gifgen.converter:convert_images_to_gif',
        ],
    },
    author='Anish Tipnis',
    author_email='rusty3699@gmail.com',
    description='A package to convert images in folders to GIFs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rusty3699/gifgen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
