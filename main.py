import streamlit as st
import pandas as pd
from insights import generate_insights  # Import AI function

st.title("📊 AI-Powered Business Insights Generator")
st.write("Upload a CSV file, and AI will generate insights.")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)  # Read file
    st.write("### Preview of Data:")
    st.dataframe(df.head())  # Show top rows

    # AI Insights Button
    if st.button("Generate Insights"):
        with st.spinner("AI is analyzing... Please wait."):
            insights = generate_insights(df)  # Call AI function
            st.write("## 🔍 AI-Generated Insights:")
            st.success(insights)  # Formats output nicely in Streamlit
