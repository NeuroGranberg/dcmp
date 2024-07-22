import os

def process_anat_folders(base_path, predictor, sample_size=None, skip_keywords=None):
    if skip_keywords is None:
        skip_keywords = []
    skip_keywords = [keyword.lower() for keyword in skip_keywords]

    results = {}
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            if any(keyword in folder_name.lower() for keyword in skip_keywords):
                continue
            
            predictions = predictor.predict_folder(folder_path, sample_size=sample_size, skip_keywords=skip_keywords)
            
            if predictions:
                avg_modality, avg_probability, valid_count = predictor.compute_average_prediction(predictions)
                results[folder_name] = {
                    'predicted_modality': avg_modality,
                    'average_probability': avg_probability,
                    'files_processed': valid_count,
                    'total_files': len(predictions)
                }
            else:
                results[folder_name] = process_subfolders(folder_path, predictor, sample_size, skip_keywords)
    
    return results

def process_subfolders(parent_folder, predictor, sample_size=None, skip_keywords=None):
    if skip_keywords is None:
        skip_keywords = []
    skip_keywords = [keyword.lower() for keyword in skip_keywords]

    results = {}
    for sub_folder_name in os.listdir(parent_folder):
        sub_folder_path = os.path.join(parent_folder, sub_folder_name)
        if os.path.isdir(sub_folder_path):
            if any(keyword in sub_folder_name.lower() for keyword in skip_keywords):
                continue
            
            predictions = predictor.predict_folder(sub_folder_path, sample_size=sample_size, skip_keywords=skip_keywords)
            
            if predictions:
                avg_modality, avg_probability, valid_count = predictor.compute_average_prediction(predictions)
                results[sub_folder_name] = {
                    'predicted_modality': avg_modality,
                    'average_probability': avg_probability,
                    'files_processed': valid_count,
                    'total_files': len(predictions)
                }
            else:
                results[sub_folder_name] = {
                    'predicted_modality': None,
                    'average_probability': None,
                    'files_processed': 0,
                    'total_files': 0,
                    'error': 'No valid DICOM files found'
                }
    
    return results