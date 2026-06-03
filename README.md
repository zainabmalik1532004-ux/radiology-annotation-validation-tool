# Radiology Image Annotation & Quality Validation Tool

A Python and Streamlit web application for annotating medical images and validating dataset quality before AI model training.

## What it does

This tool standardizes the annotation of chest X-rays and brainstem and cerebellum MRI and CT scans, and validates dataset quality before the data enters an AI model training pipeline.

It solves three core problems in radiology AI dataset preparation:
- Annotation inconsistency — different annotators labeling the same structure differently
- Missing clinical flags — abnormal findings going undetected before AI training
- Poor data quality — low-confidence or undocumented annotations reaching the model pipeline

## Features

### Chest X-Ray mode
- Upload chest X-ray images
- Label findings: Normal, Pneumonia, Pleural Effusion, Cardiomegaly
- Set confidence level and add notes

### Brainstem and Cerebellum mode
- Structures: Midbrain, Pons, Medulla Oblongata, Cerebellar Vermis, Cerebellar Hemispheres, Cerebellar Tonsils, Dentate Nucleus, Superior, Middle and Inferior Cerebellar Peduncles
- Imaging sequence: T1, T2, FLAIR, DWI and ADC, T1 with Gadolinium, CT
- Laterality field for bilateral structures (Left or Right)
- Boundary certainty flag (Certain or Uncertain)
- Clinical flags: Chiari malformation, demyelination, infarction, beam hardening artifact, asymmetry

### Validation Dashboard
- Flags low confidence annotations (below 5 out of 10)
- Flags missing notes
- Flags uncertain boundaries for escalation
- Alerts on clinical findings requiring expert review
- Summary metrics: total annotations, unique images, average confidence, clinical flag count

## Tech Stack

- Python 3.11
- Streamlit
- pandas
- Pillow
- pydicom
- numpy

## How to run

```bash
git clone https://github.com/zainabmalik1532004-ux/radiology-annotation-validation-tool.git
cd radiology-annotation-validation-tool
python3.11 -m venv venv
source venv/bin/activate
pip install streamlit pydicom pandas Pillow numpy
streamlit run app.py
```

## Documentation

Full annotation guidelines covering brainstem and cerebellum anatomy, imaging sequence rules, annotation definition refinement process, quality control criteria, and pre-handoff validation checklist.

## Author

Zainab Malik — Health Informatics, Deggendorf Institute of Technology — June 2026
