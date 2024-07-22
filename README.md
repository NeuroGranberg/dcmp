# DCMP (DICOM Modality Predictor)

DCMP is a Python package that predicts the modality of DICOM (Digital Imaging and Communications in Medicine) images using a pre-trained scikit-learn model.

## Features

- Predict modality for individual DICOM files
- Process lists of DICOM file paths
- Analyze entire directories of DICOM files, including nested subdirectories
- Option to sample a subset of files for faster processing of large datasets
- Skip specific folders based on keywords
- Multithreaded processing for improved performance
- Command-line interface for easy use
- Comprehensive error handling and reporting

## Dependencies

DCMP relies on several Python libraries and system dependencies. Here's how to install them:

### System Dependencies

On Debian-based systems (like Ubuntu), you should install the necessary system dependencies for OpenCV with the following commands:

```bash
sudo apt update
sudo apt install libopencv-dev python3-opencv
```

### Python Dependencies

The main Python dependencies are:

- numpy
- pydicom
- opencv-python
- scikit-learn==1.4.0
- joblib

```bash
pip install numpy pydicom opencv-python opencv-contrib-python scikit-learn==1.4.0 joblib
```

## Installation

You can install the DCMP package using pip:

```
pip install dcmp
```

## Usage

### Python API

#### Predicting a Single File

```python
from dcmp import DicomModalityPredictor

predictor = DicomModalityPredictor()
result = predictor.predict_single_file('/path/to/your/dicom/file.dcm')
print(result)
```

#### Predicting a List of Files

```python
from dcmp import DicomModalityPredictor

predictor = DicomModalityPredictor()

dicom_files = [
    '/path/to/file1.dcm',
    '/path/to/file2.dcm',
    '/path/to/file3.dcm',
]

results = predictor.predict_file_list(dicom_files)

for result in results:
    if result['error'] is None:
        print(f"File: {result['filename']}")
        print(f"Predicted Modality: {result['predicted_modality']}")
        print(f"Probability: {result['probability']:.4f}")
    else:
        print(f"Error processing {result['filename']}: {result['error']}")
    print("---")
```
#### Processing a single dicom series Directory

```python
from dcmp import DicomModalityPredictor

predictor = DicomModalityPredictor()

results = predictor.predict_folder('/path/to/your/dicom-folder')

for result in results:
    if result['error'] is None:
        print(f"File: {result['filename']}")
        print(f"Predicted Modality: {result['predicted_modality']}")
        print(f"Probability: {result['probability']:.4f}")
    else:
        print(f"Error processing {result['filename']}: {result['error']}")
    print("---")
```


#### Processing a BIDS anat Directory

```python
from dcmp import DicomModalityPredictor
from dcmp.utils import process_anat_folders

predictor = DicomModalityPredictor()

base_path = '/path/to/BIDS-data-dcm/anat-folder'
skip_keywords = ['localizer', 'scout', 'symri', 'swi']  # It will skip the folders that include these keywords
sample_size = 20  # Process randomly up to 20 files per folder

results = process_anat_folders(base_path, predictor, sample_size=sample_size, skip_keywords=skip_keywords)

for folder, result in results.items():
    print(f"Folder: {folder}")
    print(f"Predicted Modality: {result['predicted_modality']}")
    print(f"Average Probability: {result['average_probability']:.4f}")
    print(f"Files Processed: {result['files_processed']} / {result['total_files']}")
    print("---")
```

### Command-line Interface

The package also provides a command-line interface for easy use:

```
dcmp /path/to/dicom/folders --sample 20 --skip localizer scout symri swi --output results.json
```

Options:
- `--sample`: Number of DICOM files to sample from each folder
- `--skip`: Keywords to skip folders (can provide multiple)
- `--output`: Path to save the results JSON file
- `--model`: Path to a custom trained model file (optional)

## Customization

### Using a Custom Model

You can use your own trained scikit-learn model by providing the path to the model file:

```python
predictor = DicomModalityPredictor(model_path='/path/to/your/custom_model.pkl')
```

### Adjusting Thread Pool Size

The `predict_file_list` method uses a `ThreadPoolExecutor` for parallel processing. You can adjust the number of worker threads:

```python
results = predictor.predict_file_list(dicom_files, max_workers=4)
```

## Error Handling

The package includes comprehensive error handling. When processing multiple files, if an error occurs with one file, the package will continue processing the remaining files and include error information in the results.

## Contributing

Contributions to the DCMP package are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This package uses scikit-learn for the underlying machine learning model.
- The model is trained on KI MRI scans.
- DICOM file handling is done using the pydicom library.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.