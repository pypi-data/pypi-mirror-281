# gif-generator
 
A Python package to convert images in folders to GIFs.

## Installation

You can install the package using pip:

```bash
pip install pip install gif-generator
```

## Usage

```python
from gifgenerator import convert_images_to_gif

image_folders = ['/path/to/folder1', '/path/to/folder2']
output_folder = '/path/to/output'
convert_images_to_gif(image_folders, output_folder)
```