from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='ascii_image_art',
    version='0.0.4.7',
    description='Python library to convert images into accii chararters text file and ascii characters colored images.',
    author='Mohammad Asad',
    readme ='README.md',
    classifiers = [
    'Operating System :: OS Independent',
    'License :: OSI Approved :: BSD License',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown', 
    license='MIT',
    packages=find_packages(),
    keywords=['python','ascii','image to text','image to ascii', 'color ascii image','text image','asad','ascii_art','acii_image']
)