from setuptools import setup, find_packages

setup(
    name='gif-generator',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'gif-generator = gifgenerator.converter:convert_images_to_gif',
        ],
    },
    author='Anish Tipnis',
    author_email='rusty3699@gmaol.com',
    description='A package to convert images in folders to GIFs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rusty3699/gif-generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
