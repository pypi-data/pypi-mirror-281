from setuptools import setup, find_packages

# Read the long description from your README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='myinternshipcalculator2024',
    version='0.3.3',
    packages=find_packages(),
    install_requires=[],
    author='Abdallah Abdelsameia',
    author_email='aabdelsameia1@gmail.com',
    description='A simple internship hours calculator.',
    long_description=long_description,  # Include long description
    long_description_content_type="text/markdown",  # Specify the content type for Markdown
    url='https://github.com/aabdelsameia1/myinternshipcalculator2024',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
