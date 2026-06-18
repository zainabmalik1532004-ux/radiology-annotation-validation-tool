Radiology Image Annotation & Quality Validation Tool

A Python and Streamlit web application for annotating medical images and validating dataset quality before AI model training.

What it does

This tool standardizes the annotation of chest X-rays and brainstem and cerebellum MRI and CT scans, and validates dataset quality before the data enters an AI model training pipeline.

It solves three core problems in radiology AI dataset preparation:


Annotation inconsistency — different annotators labeling the same structure differently
Missing clinical flags — abnormal findings going undetected before AI training
Poor data quality — low-confidence or undocumented annotations reaching the model pipeline


Features

Chest X-Ray mode


Upload chest X-ray images
Label findings: Normal, Pneumonia, Pleural Effusion, Cardiomegaly
Set confidence level and add notes


Brainstem and Cerebellum mode


Structures: Midbrain, Pons, Medulla Oblongata, Cerebellar Vermis, Cerebellar Hemispheres, Cerebellar Tonsils, Dentate Nucleus, Superior, Middle and Inferior Cerebellar Peduncles
Imaging sequence: T1, T2, FLAIR, DWI and ADC, T1 with Gadolinium, CT
Laterality field for bilateral structures (Left or Right)
Boundary certainty flag (Certain or Uncertain)
Clinical flags: Chiari malformation, demyelination, infarction, beam hardening artifact, asymmetry


Validation Dashboard


Flags low confidence annotations (below 5 out of 10)
Flags missing notes
Flags uncertain boundaries for escalation
Alerts on clinical findings requiring expert review
Summary metrics: total annotations, unique images, average confidence, clinical flag count


Tech Stack


Python 3.11
Streamlit
pandas
Pillow
pydicom
numpy
pytest (testing)
GitHub Actions (CI/CD)


How to run

bashgit clone https://github.com/zainabmalik1532004-ux/radiology-annotation-validation-tool.git
cd radiology-annotation-validation-tool
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

Or use the helper script, which sets up the environment, runs the tests, and launches the app in one step:

bashbash run.sh

Testing & CI/CD

The annotation quality rules are separated into independent, testable functions in validation.py, so each rule can be verified automatically rather than by manual clicking.


Automated tests (test_validation.py) cover every validation rule — low-confidence detection, missing-notes detection, uncertain-boundary flags, and clinical-flag handling. Run them with:


bash  pytest -v


Shell script (run.sh) automates environment setup, test execution, and app launch.
Continuous Integration (.github/workflows/ci.yml) runs the full test suite automatically on every push using GitHub Actions, on a clean Python 3.11 environment. This ensures the validation logic stays correct as the project evolves.


Annotation Guidelines Document

A full annotation guidelines document is included in this repository covering:


Brainstem and cerebellum anatomical overview with landmark definitions
Imaging sequence rules for MRI and CT (T1, T2, FLAIR, DWI and ADC, T1 with Gadolinium)
Annotation definition rules for every structure
Annotation review checklist with pass, fail, and flag criteria
Annotation definition refinement process
Common annotation errors and prevention
Pre-handoff validation checklist requiring Dice coefficient above 0.80 for inter-annotator agreement


Download PDF: Radiology_AI_Annotation_Project.pdf
Download Word: Radiology_AI_Annotation_Project.docx


Note: This is an educational and portfolio project. The annotation guidelines were compiled from neuroanatomy textbooks, radiology literature, and imaging references, and have not been clinically validated by a radiologist. They are intended to demonstrate annotation-review and data-quality methodology, not for clinical use.



Author

Zainab Malik — Health Informatics, Deggendorf Institute of Technology — June 2026
