import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="B-UML Dataset Explorer", layout="wide")

st.title("B-UML Dataset Explorer")

# -------------------------
# Load data
# -------------------------

@st.cache_data
def load_data():
    with open("dataset.json") as f:
        return pd.DataFrame(json.load(f))

df = load_data()

# -------------------------
# Sidebar filters
# -------------------------

st.sidebar.header("Filters")

dataset_filter = st.sidebar.selectbox(
    "Dataset",
    ["All"] + sorted(df["dataset"].unique())
)

category_filter = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique())
)

if dataset_filter != "All":
    df = df[df["dataset"] == dataset_filter]

if category_filter != "All":
    df = df[df["category"] == category_filter]

# -------------------------
# Metrics
# -------------------------

st.header("Dataset Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Models", len(df))
col2.metric("Total Classes", int(df["classes"].sum()))
col3.metric("Total Attributes", int(df["attributes"].sum()))

# -------------------------
# Distribution chart
# -------------------------

st.header("Element Distribution")

totals = df[
    ["classes","attributes","enumerations","functions","generalisations"]
].sum()

fig, ax = plt.subplots()

bars = ax.bar(totals.index, totals.values)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2,
            height,
            int(height),
            ha="center")

ax.grid(axis="y", linestyle="--", alpha=0.6)

st.pyplot(fig)

# -------------------------
# Table
# -------------------------

st.header("Models")

search = st.text_input("Search model")

if search:
    df = df[df["model"].str.contains(search, case=False)]

st.dataframe(df)