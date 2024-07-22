import os
import numpy as np
import pydicom
import cv2
import joblib
from sklearn.base import BaseEstimator
from collections import Counter
import pkg_resources
from concurrent.futures import ThreadPoolExecutor, as_completed
from pkg_resources import resource_filename

class DicomModalityPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = resource_filename('dcmp', '../model/mlp_9998.pkl')
        self.model = joblib.load(model_path)
        if not isinstance(self.model, BaseEstimator):
            raise ValueError("The loaded model is not a scikit-learn estimator.")

    def predict_single_file(self, file_path):
        try:
            dicom = pydicom.dcmread(file_path)
            image = dicom.pixel_array
            image = cv2.resize(image, (128, 128))
            image_flat = image.reshape(1, -1)
            
            prediction = self.model.predict(image_flat)
            probability = np.max(self.model.predict_proba(image_flat))
            
            return {
                'filename': os.path.basename(file_path),
                'predicted_modality': "sc" if prediction > 0.5 else "br",
                'probability': float(probability),
                'error': None
            }
        except Exception as e:
            return {
                'filename': os.path.basename(file_path),
                'predicted_modality': None,
                'probability': None,
                'error': str(e)
            }

    def predict_file_list(self, file_paths, max_workers=None):
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(self.predict_single_file, file_path): file_path for file_path in file_paths}
            for future in as_completed(future_to_file):
                results.append(future.result())
        return results

    def predict_folder(self, folder_path, sample_size=None, skip_keywords=None):
        if skip_keywords is None:
            skip_keywords = []
        skip_keywords = [keyword.lower() for keyword in skip_keywords]

        dicom_files = []
        for root, dirs, files in os.walk(folder_path):
            # Skip directories containing any of the skip keywords
            dirs[:] = [d for d in dirs if not any(keyword in d.lower() for keyword in skip_keywords)]
            
            for file in files:
                if file.endswith('.dcm'):
                    dicom_files.append(os.path.join(root, file))
        
        if sample_size and sample_size < len(dicom_files):
            dicom_files = np.random.choice(dicom_files, size=sample_size, replace=False)
        
        return self.predict_file_list(dicom_files)
    
    def predict_mean_file_list(self, file_paths, sample_size=None, max_workers=None):
        if sample_size and sample_size < len(file_paths):
            sampled_files = np.random.choice(file_paths, size=sample_size, replace=False)
        else:
            sampled_files = file_paths

        results = self.predict_file_list(sampled_files, max_workers=max_workers)
        return self.compute_average_prediction(results)

    @staticmethod
    def compute_average_prediction(predictions):
        valid_predictions = [pred for pred in predictions if pred['predicted_modality'] is not None]
        if not valid_predictions:
            return None, 0, len(predictions)

        modalities = [pred['predicted_modality'] for pred in valid_predictions]
        probabilities = [pred['probability'] for pred in valid_predictions]
        
        modality_counts = Counter(modalities)
        average_modality = modality_counts.most_common(1)[0][0]
        average_probability = np.mean(probabilities)
        
        return average_modality, average_probability, len(valid_predictions)