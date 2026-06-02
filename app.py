import streamlit as st
from PIL import Image
import pandas as pd
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="Radiology Annotation Tool", layout="wide")

# Title
st.title("Radiology Image Annotation & Quality Validation Tool")
st.markdown("Annotate chest X-ray images and validate dataset quality for AI model training.")

# Create folders if they don't exist
os.makedirs("sample_images", exist_ok=True)
os.makedirs("annotations", exist_ok=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload & Annotate", "Validation Dashboard"])

if page == "Upload & Annotate":
    st.header("Upload & Annotate X-Ray Images")
    
    uploaded_file = st.file_uploader("Upload a chest X-ray image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-Ray", width=600)
        
        st.subheader("Add Annotation")
        label = st.selectbox("Select finding", ["Normal", "Pneumonia", "Pleural Effusion", "Cardiomegaly", "Other"])
        confidence = st.slider("Confidence level", 1, 10, 5)
        notes = st.text_area("Notes")
        
        if st.button("Save Annotation"):
            annotation = {
                "filename": uploaded_file.name,
                "label": label,
                "confidence": confidence,
                "notes": notes,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            df_new = pd.DataFrame([annotation])
            csv_path = "annotations/annotations.csv"
            if os.path.exists(csv_path):
                df_existing = pd.read_csv(csv_path)
                df = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df = df_new
            df.to_csv(csv_path, index=False)
            st.success("Annotation saved successfully!")

elif page == "Validation Dashboard":
    st.header("Validation Dashboard")
    
    csv_path = "annotations/annotations.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        st.subheader("All Annotations")
        st.table(df)
        
        st.subheader("Quality Checks")
        low_confidence = df[df["confidence"] < 5]
        missing_notes = df[df["notes"].isna() | (df["notes"] == "")]
        
        if len(low_confidence) > 0:
            st.warning(f"{len(low_confidence)} annotation(s) have low confidence (below 5)")
        if len(missing_notes) > 0:
            st.warning(f"{len(missing_notes)} annotation(s) have no notes")
        if len(low_confidence) == 0 and len(missing_notes) == 0:
            st.success("All annotations passed quality checks!")
        
        st.subheader("Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Annotations", len(df))
        col2.metric("Unique Images", df["filename"].nunique())
        col3.metric("Avg Confidence", round(df["confidence"].mean(), 1))
    else:
        st.info("No annotations yet. Upload and annotate images first.")