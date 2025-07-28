use aiml_placement_app
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    gender VARCHAR(10),
    college VARCHAR(100),
    degree VARCHAR(50),
    graduation_year INT,
    cgpa FLOAT
);
CREATE TABLE programming_skills (
    student_id INT,
    problems_solved INT,
    mini_projects INT,
    certifications_earned INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
CREATE TABLE soft_skills (
    student_id INT,
    communication_score INT,
    teamwork_score INT,
    presentation_score INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
CREATE TABLE placements (
    student_id INT,
    mock_interview_score INT,
    internships_completed INT,
    placed BOOLEAN,
    company VARCHAR(100),
    salary INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);