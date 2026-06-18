"""
test_validation.py
Automatic tests for the validation rules.
Run them by typing:  pytest
Every function that starts with test_ is one automatic check.
"""

from validation import (
    is_low_confidence,
    has_missing_notes,
    is_uncertain_boundary,
    has_clinical_flag,
    validate_annotation,
)

# --- confidence checks ---
def test_low_confidence_is_flagged():
    assert is_low_confidence(3) == True

def test_high_confidence_is_not_flagged():
    assert is_low_confidence(8) == False

def test_confidence_exactly_5_passes():
    assert is_low_confidence(5) == False

# --- notes checks ---
def test_empty_notes_flagged():
    assert has_missing_notes("") == True

def test_spaces_only_notes_flagged():
    assert has_missing_notes("   ") == True

def test_real_notes_not_flagged():
    assert has_missing_notes("Lesion in left hemisphere") == False

# --- boundary checks ---
def test_uncertain_boundary_flagged():
    assert is_uncertain_boundary("Uncertain") == True

def test_certain_boundary_not_flagged():
    assert is_uncertain_boundary("Certain") == False

# --- clinical flag checks ---
def test_clinical_flag_present():
    assert has_clinical_flag("Chiari malformation") == True

def test_no_clinical_flag():
    assert has_clinical_flag("None") == False

# --- all rules together ---
def test_good_annotation_has_no_issues():
    good = {
        "confidence": 9,
        "notes": "Clear T2 image, normal dentate nucleus",
        "boundary": "Certain",
        "clinical_flag": "None",
    }
    assert validate_annotation(good) == []

def test_bad_annotation_collects_all_issues():
    bad = {
        "confidence": 2,
        "notes": "",
        "boundary": "Uncertain",
        "clinical_flag": "Infarction",
    }
    assert len(validate_annotation(bad)) == 4
