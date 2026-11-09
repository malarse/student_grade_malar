
import streamlit as st
import pandas as pd

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------
# CUSTOM DESIGN
# --------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #263750);
    color: white;
}

.main-title {
    font-size: 38px;
    font-weight: bold;
    color: #a78bfa;
}

.subtitle {
    color: #cbd5e1;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: #293b55;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #64748b;
}

div[data-testid="stMetricLabel"] {
    color: #c4b5fd;
}

div[data-testid="stMetricValue"] {
    color: white;
}

div.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #6366f1);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# HEADER
# --------------------------------
st.markdown(
    '<div class="main-title">🎓 Student Grade Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Manage students | Track grades | Analyze performance</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------
# GRADING LOGIC - DAY 2
# --------------------------------
def get_grade(mark):

    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# --------------------------------
# SESSION STATE
# --------------------------------
if "students" not in st.session_state:
    st.session_state.students = []


# --------------------------------
# ADD STUDENT FORM
# --------------------------------
with st.sidebar:

    st.header("➕ Add New Student")
    st.write("Enter student information.")

    with st.form("student_form", clear_on_submit=True):

        name = st.text_input("Student Name")

        mark = st.number_input(
            "Enter Mark",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

        submit = st.form_submit_button(
            "Add Student",
            width="stretch"
        )

        if submit:

            if not name.strip():
                st.error("Please enter student name.")

            elif any(
                student["Name"].lower() == name.strip().lower()
                for student in st.session_state.students
            ):
                st.warning("Student already exists.")

            else:

                grade = get_grade(mark)

                student = {
                    "Name": name.strip(),
                    "Mark": mark,
                    "Grade": grade
                }

                st.session_state.students.append(student)

                st.success(f"{name} added successfully!")
                st.rerun()


# --------------------------------
# STUDENT DATA
# --------------------------------
students = st.session_state.students

if students:

    df = pd.DataFrame(students)
    marks = df["Mark"]

    total_students = len(df)
    average = marks.mean()
    highest = marks.max()
    lowest = marks.min()

else:

    df = pd.DataFrame(columns=["Name", "Mark", "Grade"])

    total_students = 0
    average = 0
    highest = 0
    lowest = 0


# --------------------------------
# CLASS PERFORMANCE
# --------------------------------
st.subheader("📊 Class Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("📈 Average Marks", f"{average:.2f}")
col3.metric("🏆 Highest Marks", highest)
col4.metric("📉 Lowest Marks", lowest)


st.divider()


# --------------------------------
# STUDENT RESULTS
# --------------------------------
st.subheader("📋 Student Results")

if not df.empty:

    search = st.text_input(
        "🔍 Search Student",
        placeholder="Enter student name..."
    )

    filtered_df = df[
        df["Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True
    )

    # Download student report
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Student Report",
        data=csv,
        file_name="student_results.csv",
        mime="text/csv"
    )

else:

    st.info("No students added yet. Add your first student using the sidebar.")


st.divider()


# --------------------------------
# GRADE ANALYSIS
# --------------------------------
st.subheader("📈 Grade Performance Analysis")

if not df.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.write("Grade Distribution")

        grade_counts = (
            df["Grade"]
            .value_counts()
            .reindex(["A", "B", "C", "D", "F"], fill_value=0)
        )

        st.bar_chart(grade_counts)

    with col2:

        st.write("Grade Summary")

        for grade in ["A", "B", "C", "D", "F"]:

            count = (df["Grade"] == grade).sum()

            st.write(f"Grade {grade}: {count} students")

            st.progress(count / total_students)

else:

    st.info("Add student records to see grade analytics.")


# --------------------------------
# CLEAR STUDENT RECORDS
# --------------------------------
st.divider()

if students:

    if st.button("🗑️ Clear All Records"):

        st.session_state.students = []
        st.rerun()


# --------------------------------
# FOOTER
# --------------------------------
st.markdown("---")

st.markdown(
    "<center style='color:#94a3b8;'>"
    "Made with ❤️ using Python, Pandas & Streamlit"
    "</center>",
    unsafe_allow_html=True
)
