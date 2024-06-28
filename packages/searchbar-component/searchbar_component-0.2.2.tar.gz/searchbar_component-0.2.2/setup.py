from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='searchbar_component',
    version='0.2.2',
    description='A Streamlit component for a search bar with autosuggestions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chris weeks',  
    url='https://github.com/weeks888/searchbar_component',  # Replace with your repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit>=0.63',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    license='MIT',
    keywords='streamlit component searchbar autocomplete',
)
