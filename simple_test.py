import os
os.environ["CHROMA_DB_IMPL"] = "duckdb"

import streamlit as st

st.title("🚀 Simple Test App")
st.write("If you can see this, Streamlit is working!")
st.success("✅ ChromaDB SQLite fix is working")

if st.button("Test Button"):
    st.balloons()
    st.write("Button clicked successfully!")