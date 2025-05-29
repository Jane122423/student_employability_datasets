import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Student-Employability-Datasets.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Define score columns
score_columns = [
    "GENERAL APPEARANCE",
    "MANNER OF SPEAKING",
    "PHYSICAL CONDITION",
    "MENTAL ALERTNESS",
    "SELF-CONFIDENCE",
    "ABILITY TO PRESENT IDEAS",
    "COMMUNICATION SKILLS"
]

# Page Title
st.title("🎓 Student Employability Dashboard")

# Dropdown: Select student
student_names = df["Name of Student"].dropna().unique().tolist()
student_name = st.selectbox("Select Student", ["All"] + student_names)

# Bar chart of student scores or overall distribution
if student_name != "All":
    student_data = df[df["Name of Student"] == student_name]
    melted = student_data.melt(
        id_vars=["Name of Student"],
        value_vars=score_columns,
        var_name="Skill",
        value_name="Score"
    )
    fig = px.bar(
        melted,
        x="Skill",
        y="Score",
        color="Skill",
        title=f"Scores for {student_name}"
    )
else:
    fig = px.histogram(
        df,
        x="CLASS",
        color="CLASS",
        title="Employability Class Distribution"
    )

st.plotly_chart(fig, use_container_width=True)

# Average Skill Scores by Class
avg_scores = df.groupby("CLASS")[score_columns].mean(numeric_only=True).reset_index()
avg_melted = avg_scores.melt(id_vars="CLASS", var_name="Skill", value_name="Average Score")

fig2 = px.bar(
    avg_melted,
    x="Skill",
    y="Average Score",
    color="CLASS",
    barmode="group",
    title="Average Skill Scores by Class"
)
st.plotly_chart(fig2, use_container_width=True)

# Correlation Heatmap
st.subheader("📊 Correlation Heatmap of Skill Scores")
try:
    corr = df[score_columns].corr(numeric_only=True)
    fig3 = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap",
        aspect="auto"
    )
    st.plotly_chart(fig3, use_container_width=True)
except Exception as e:
    st.error(f"Unable to generate heatmap: {e}")
