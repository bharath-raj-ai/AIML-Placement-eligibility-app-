import streamlit as st
import mysql.connector
import pandas as pd
from faker import Faker
import random

fake = Faker()
num_students = 50


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="900380Bha@", 
    database="aiml_placement_app"
)
cursor = conn.cursor()


cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DELETE FROM programming_skills")
cursor.execute("DELETE FROM soft_skills")
cursor.execute("DELETE FROM placements")
cursor.execute("DELETE FROM students")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


for i in range(1, num_students + 1):
    name = fake.name()
    email = fake.email()
    phone = fake.msisdn()[:10]
    gender = random.choice(["Male", "Female"])
    college = fake.company() + " Institute"
    degree = random.choice(["B.Tech", "B.Sc", "BCA", "BE"])
    grad_year = random.choice([2022, 2023, 2024])
    cgpa = round(random.uniform(6.0, 9.8), 2)

    cursor.execute("""
        INSERT INTO students (student_id, name, email, phone, gender, college, degree, graduation_year, cgpa)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (i, name, email, phone, gender, college, degree, grad_year, cgpa))

    cursor.execute("""
        INSERT INTO programming_skills (student_id, problems_solved, mini_projects, certifications_earned)
        VALUES (%s, %s, %s, %s)
    """, (
        i,
        random.randint(20, 300),
        random.randint(0, 5),
        random.randint(0, 3)
    ))

    cursor.execute("""
        INSERT INTO soft_skills (student_id, communication_score, teamwork_score, presentation_score)
        VALUES (%s, %s, %s, %s)
    """, (
        i,
        random.randint(40, 100),
        random.randint(40, 100),
        random.randint(40, 100)
    ))

    placed = random.choice([True, False])
    mock_score = random.randint(40, 100)
    internships = random.randint(0, 3)
    company = fake.company() if placed else ""
    salary = random.randint(300000, 1200000) if placed else 0

    cursor.execute("""
        INSERT INTO placements (student_id, mock_interview_score, internships_completed, placed, company, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (i, mock_score, internships, placed, company, salary))

conn.commit()
cursor.close()
conn.close()

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title(" Placement Eligibility App (GUVI Project)")
st.write("Check eligibility of students based on placement criteria (SQL filtered)")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="900380Bha@", 
    database="aiml_placement_app"
)


st.sidebar.header(" Set Eligibility Filters")
min_cgpa = st.sidebar.slider("Minimum CGPA", 6.0, 10.0, 7.0)
min_problems = st.sidebar.slider("Minimum Problems Solved", 0, 300, 50)
min_comm = st.sidebar.slider("Minimum Communication Score", 0, 100, 60)
min_mock = st.sidebar.slider("Minimum Mock Interview Score", 0, 100, 60)

if st.sidebar.button("Find Eligible Students"):
    query = f"""
        SELECT s.student_id, s.name, s.email, s.cgpa,
               pr.problems_solved, ss.communication_score,
               p.mock_interview_score, pl.placed, pl.company, pl.salary
        FROM students s
        JOIN programming_skills pr ON s.student_id = pr.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN placements p ON s.student_id = p.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE s.cgpa >= {min_cgpa}
          AND pr.problems_solved >= {min_problems}
          AND ss.communication_score >= {min_comm}
          AND p.mock_interview_score >= {min_mock}
          AND pl.placed = 1
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results)

    st.subheader(" Eligible Students")
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning(" No students match the criteria.")
    cursor.close()

st.markdown("---")
st.subheader(" Placement Insights (SQL Based)")

insight_queries = {
    "Total Students": "SELECT COUNT(*) AS result FROM students;",
    "Average CGPA": "SELECT ROUND(AVG(cgpa), 2) AS result FROM students;",
    "Highest Mock Interview Score": "SELECT MAX(mock_interview_score) AS result FROM placements;",
    "Average Problems Solved": "SELECT ROUND(AVG(problems_solved), 2) AS result FROM programming_skills;",
    "Students Placed": "SELECT COUNT(*) AS result FROM placements WHERE placed = 1;",
    "Top 5 Students by CGPA": "SELECT name, cgpa FROM students ORDER BY cgpa DESC LIMIT 5;",
    "Avg Communication Score": "SELECT ROUND(AVG(communication_score), 2) AS result FROM soft_skills;",
    "Most Common Degree": "SELECT degree, COUNT(*) AS count FROM students GROUP BY degree ORDER BY count DESC LIMIT 1;",
    "Highest Salary Offered": "SELECT MAX(salary) AS result FROM placements;",
    "Avg Internships Completed": "SELECT ROUND(AVG(internships_completed), 2) AS result FROM placements;"
}

for title, query in insight_queries.items():
    st.markdown(f"#### {title}")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result)
    st.dataframe(df)
    cursor.close()

conn.close()
