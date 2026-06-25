import streamlit as st
from PIL import Image
import pandas as pd
import os
from datetime import datetime
from db import insert_annotation, fetch_annotations_df, update_annotation_metadata

# Page setup
st.set_page_config(page_title="Radiology Annotation Tool", layout="wide")

# Title
st.title("Radiology Image Annotation & Quality Validation Tool")
st.markdown("Annotate medical images and validate dataset quality for AI model training.")


# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload & Annotate", "Validation Dashboard"])

# Scan type selection in sidebar
st.sidebar.markdown("---")
st.sidebar.title("Scan Type")
scan_type = st.sidebar.radio("Select scan type", ["Chest X-Ray", "Brainstem & Cerebellum"])

if page == "Upload & Annotate":
    st.header(f"Upload & Annotate — {scan_type}")

    uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=600)

        st.subheader("Add Annotation")

        if scan_type == "Chest X-Ray":
            label = st.selectbox("Select finding", [
                "Normal",
                "Pneumonia",
                "Pleural Effusion",
                "Cardiomegaly",
                "Other"
            ])
            sequence = st.selectbox("Imaging type", ["X-Ray"])
            side = "N/A"
            boundary_flag = "Certain"
            clinical_flag = "None"

        else:  # Brainstem & Cerebellum
            structure = st.selectbox("Select structure", [
                "Midbrain",
                "Pons",
                "Medulla Oblongata",
                "Cerebellar Vermis",
                "Cerebellar Hemisphere",
                "Cerebellar Tonsils",
                "Dentate Nucleus",
                "Superior Cerebellar Peduncle",
                "Middle Cerebellar Peduncle",
                "Inferior Cerebellar Peduncle"
            ])
            label = structure

            sequence = st.selectbox("Imaging sequence", [
                "T1-weighted",
                "T2-weighted",
                "FLAIR",
                "DWI/ADC",
                "T1 + Gadolinium",
                "CT"
            ])

            # Bilateral structures need left/right
            bilateral = ["Cerebellar Hemisphere", "Dentate Nucleus",
                        "Superior Cerebellar Peduncle",
                        "Middle Cerebellar Peduncle",
                        "Inferior Cerebellar Peduncle"]

            if structure in bilateral:
                side = st.selectbox("Side", ["Left", "Right"])
            else:
                side = "N/A"

            boundary_flag = st.selectbox("Boundary certainty", [
                "Certain",
                "Uncertain — needs review"
            ])

            clinical_flag = st.selectbox("Clinical flag", [
                "None",
                "Tonsil descent > 5mm — possible Chiari Type I",
                "Possible demyelination",
                "Possible infarction",
                "Beam hardening artifact — do not label",
                "Asymmetry detected — flag for review",
                "Other abnormality"
            ])

        confidence = st.slider("Confidence level (1-10)", 1, 10, 5)
        notes = st.text_area("Notes")

        if st.button("Save Annotation"):
            annotation = {
                "scan_type": scan_type,
                "filename": uploaded_file.name,
                "label": label,
                "sequence": sequence,
                "side": side,
                "boundary_flag": boundary_flag,
                "clinical_flag": clinical_flag,
                "confidence": confidence,
                "notes": notes,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            insert_annotation(annotation)
            st.success("Annotation saved successfully!")

elif page == "Validation Dashboard":
    st.header("Validation Dashboard")

    # Filter by scan type
    st.subheader("Filter by Scan Type")
    filter_type = st.radio("Show", ["All", "Chest X-Ray", "Brainstem & Cerebellum"])
    df = fetch_annotations_df(filter_type)

    if not df.empty:
        st.subheader("All Annotations")
        st.table(df)

        st.subheader("Correct Metadata")
        st.caption("Fix a label, confidence score, or note on a flagged entry.")
        row_options = [f"{row['filename']} — {row['timestamp']}" for _, row in df.iterrows()]
        selected = st.selectbox("Select entry to correct", row_options)
        selected_row = df.iloc[row_options.index(selected)]

        with st.form("correct_metadata_form"):
            new_label = st.text_input("Label", value=selected_row["label"])
            new_confidence = st.slider("Confidence level (1-10)", 1, 10, int(selected_row["confidence"]))
            new_notes = st.text_area("Notes", value=selected_row["notes"])

            if st.form_submit_button("Save Correction"):
                update_annotation_metadata(
                    filename=selected_row["filename"],
                    timestamp=selected_row["timestamp"],
                    updates={"label": new_label, "confidence": new_confidence, "notes": new_notes}
                )
                st.success("Metadata corrected. Refresh the page to see the update.")

        st.subheader("Quality Checks")
        issues = 0

        low_confidence = df[df["confidence"] < 5]
        if len(low_confidence) > 0:
            st.warning(f"⚠️ {len(low_confidence)} annotation(s) with low confidence (below 5)")
            issues += 1

        missing_notes = df[df["notes"].isna() | (df["notes"] == "")]
        if len(missing_notes) > 0:
            st.warning(f"⚠️ {len(missing_notes)} annotation(s) with no notes")
            issues += 1

        if "boundary_flag" in df.columns:
            uncertain = df[df["boundary_flag"] == "Uncertain — needs review"]
            if len(uncertain) > 0:
                st.warning(f"⚠️ {len(uncertain)} annotation(s) have uncertain boundaries")
                issues += 1

        if "clinical_flag" in df.columns:
            flagged = df[df["clinical_flag"] != "None"]
            if len(flagged) > 0:
                st.error(f"🚨 {len(flagged)} annotation(s) have clinical flags — review required")
                issues += 1

        if issues == 0:
            st.success("All annotations passed quality checks!")

        st.subheader("Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Annotations", len(df))
        col2.metric("Unique Images", df["filename"].nunique())
        col3.metric("Avg Confidence", round(df["confidence"].mean(), 1))
        col4.metric("Clinical Flags", len(df[df["clinical_flag"] != "None"]) if "clinical_flag" in df.columns else 0)

    else:
        st.info("No annotations yet. Upload and annotate images first.")