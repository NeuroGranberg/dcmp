import argparse
import json
from .predictor import DicomModalityPredictor
from .utils import process_anat_folders

def main():
    parser = argparse.ArgumentParser(description="DICOM Modality Predictor")
    parser.add_argument("base_path", help="Path to the base folder containing DICOM files")
    parser.add_argument("--model", help="Path to the trained model file (optional)")
    parser.add_argument("--sample", type=int, help="Number of DICOM files to sample from each folder")
    parser.add_argument("--skip", nargs="*", help="Keywords to skip folders")
    parser.add_argument("--output", help="Path to save the results JSON file")

    args = parser.parse_args()

    predictor = DicomModalityPredictor(model_path=args.model)
    results = process_anat_folders(args.base_path, predictor, sample_size=args.sample, skip_keywords=args.skip)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()