from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dcmp",
    version="0.1.2",  # Increment the version number
    author="Nima Ch",
    author_email="nima.ch@gmail.com",
    description="A package to predict DICOM image modalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuroGranberg/dcmp",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dcmp': ['../model/*.pkl'],  # This will include the model file
    },
    install_requires=[
        'numpy',
        'pydicom',
        'opencv-python',
        'scikit-learn==1.4.0',
        'joblib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dcmp=dcmp.cli:main',
        ],
    },
)