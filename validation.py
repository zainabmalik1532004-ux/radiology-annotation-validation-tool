"""
validation.py
Annotation quality rules for the Radiology Annotation & Validation Tool.
Each rule is a small, independent function so it can be tested automatically.
"""

CONFIDENCE_THRESHOLD = 5


def is_low_confidence(confidence, threshold=CONFIDENCE_THRESHOLD):
    """Return True if a confidence score is below the acceptable threshold."""
    return confidence < threshold


def has_missing_notes(notes):
    """Return True if the notes field is empty or only spaces."""
    if notes is None:
        return True
    return notes.strip() == ""


def is_uncertain_boundary(boundary_flag):
    """Return True if the annotator marked the boundary as uncertain."""
    return str(boundary_flag).strip().lower() == "uncertain"


def has_clinical_flag(clinical_flag):
    """Return True if a clinical flag other than 'None' is present."""
    if clinical_flag is None:
        return False
    return str(clinical_flag).strip().lower() != "none"


def validate_annotation(annotation):
    """
    Check one annotation (a dictionary) against all rules.
    Returns a list of problem messages. An empty list means it passed everything.
    """
    issues = []
    if is_low_confidence(annotation.get("confidence", 0)):
        issues.append("Low confidence (below 5)")
    if has_missing_notes(annotation.get("notes", "")):
        issues.append("Missing notes")
    if is_uncertain_boundary(annotation.get("boundary", "")):
        issues.append("Uncertain boundary - needs review")
    if has_clinical_flag(annotation.get("clinical_flag", "None")):
        issues.append("Clinical flag - expert review required")
    return issues