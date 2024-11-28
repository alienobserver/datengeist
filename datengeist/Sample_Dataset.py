import math
import random
import pandas as pd
import streamlit as st

from datengeist.utils.helper import get_n_rows_features_csv
from datengeist.utils.style import add_top_margin_div
from datengeist.config.config import set_layout, init_uploader, init_db

def sample_dataset(uploaded_file):
    """
    Displays the dataset sampling page with options for sample size, preview, and dataset metadata.

    Parameters:
    - uploaded_file (UploadedFile): The file uploaded by the user, containing the dataset to be sampled.
    """
    st.header("Sample the Dataset")

    # Check if a dataset file has been uploaded
    if uploaded_file is not None:
        # Retrieve dataset dimensions (number of rows and features)
        n_rows, n_features = get_n_rows_features_csv(uploaded_file)

        # Add visual spacing for UI alignment
        add_top_margin_div(50)

        # Define layout columns
        cols = st.columns(4, gap='large')

        # Column 1: Dataset Instances and Sampling Percentage
        with cols[0]:
            st.metric("Dataset Instances", n_rows)
            add_top_margin_div(40)

            # Toggle to keep the entire dataset or sample
            keep_all_db = st.toggle("Keep all")

            # Slider to select sample percentage, disabled if "Keep all" is selected
            sample_pct = st.slider(
                "Sample Size (Percentage)",
                min_value=0.01,
                max_value=1.0,
                value=0.1,
                disabled=keep_all_db
            )

        # Column 2: Dataset Features and Sampling Button
        with cols[1]:
            st.metric("Number of Features", n_features)
            add_top_margin_div(80)

            # Button to initiate sampling process
            sample_button = st.button("Sample")

        # Column 3: Post-sampling Metadata and Sampling Progress Text
        with cols[2]:
            # Calculate sample size based on percentage or total dataset size if "Keep all" is selected
            sample_size = n_rows if keep_all_db else math.floor(n_rows * sample_pct)

            st.metric("Instances After Sampling", sample_size)
            add_top_margin_div(82)

            # Display progress text and update on sampling completion
            progress_text = "Click the \"Sample\" button to sample the data."

            if sample_button:
                uploaded_file.seek(0)

                if keep_all_db:
                    # Load the entire dataset if "Keep all" is selected
                    if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        dataframe = pd.read_excel(uploaded_file)
                    elif uploaded_file.type == 'text/csv':
                        print(uploaded_file)
                        dataframe = pd.read_csv(uploaded_file)
                else:
                    # Randomly select rows to skip to create a sampled subset
                    skip = sorted(random.sample(range(1, n_rows), n_rows - sample_size))

                    # Ensure the header row is not skipped
                    if 1 in skip:
                        skip.pop(skip.index(1))

                    if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        dataframe = pd.read_excel(uploaded_file, skiprows=skip)
                    elif uploaded_file.type == 'text/csv':
                        dataframe = pd.read_csv(uploaded_file, skiprows=skip)

                # Store sampled dataset in session state for later access
                st.session_state['sampled_df'] = dataframe
                progress_text = "Dataset has been sampled successfully."

            st.write(progress_text)

        # Column 4: Display estimated size of the sampled dataset
        with cols[3]:
            # Estimate dataset size in bytes after sampling
            db_size_bytes = uploaded_file.size if keep_all_db else (sample_size / n_rows * uploaded_file.size)
            db_size_mb = db_size_bytes / (1024 * 1024)

            st.metric("Dataset Size After Sampling", f"{db_size_mb:.3f} MB")

        add_top_margin_div(50)

        # Display a preview of the sampled dataset and navigation if sampling is completed
        if sample_button:
            st.write(dataframe.head())

            add_top_margin_div(50)
            cols = st.columns(6, gap='large')

            # Provide a link to navigate to the "General Info" page
            with cols[5]:
                st.page_link("pages/1_General_Info.py", label="Next")

    else:
        # Prompt to upload a dataset if none is provided
        st.subheader("Upload a dataset to start sampling!")

if __name__ == "__main__":
    set_layout()
    init_uploader()
    init_db()

    sample_dataset(st.session_state['uploaded_file'])