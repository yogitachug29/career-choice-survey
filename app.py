from flask import Flask, request, render_template, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = "career_data.csv"


def create_csv():

    if not os.path.exists(CSV_FILE):

        headers = [
            "Name",
            "Phone Number",
            "Age",
            "Study Year",

            "Career",
            "Specialization",
            "Career Clarity",
            "Reasons",
            "Who Helped",

            "Salary Importance",
            "Job Opportunity Importance",
            "Job Security Importance",
            "Career Growth Importance",
            "Interest Importance",
            "Work Life Balance Importance",
            "Respect Importance",

            "Weekly Learning Hours",
            "Certificate",
            "Internship",
            "Project",

            "After College",
            "Preferred Work Location",
            "Expected Starting Salary",

            # Employee details
            "Currently Working",
            "Current Job",
            "Current Industry",
            "Years of Experience",
            "Current Salary",
            "Did Current Career Match Childhood/Student Choice",
            "Employee Career Change"
        ]

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerow(headers)


@app.route("/")
def home():

    return render_template("careerform.html")


@app.route("/submit", methods=["POST"])
def submit():

    # -------------------------
    # BASIC DETAILS
    # -------------------------

    name = request.form.get("name", "")
    phone = request.form.get("phone", "")
    age = request.form.get("age", "")
    study_year = request.form.get("study_year", "")


    # -------------------------
    # CAREER DETAILS
    # -------------------------

    career = request.form.get("career", "")
    specialization = request.form.get("specialization", "")

    career_clarity = request.form.get(
        "career_clarity",
        ""
    )

    reasons = request.form.getlist("reason")
    reasons = ", ".join(reasons)

    who_helped = request.form.get(
        "who_helped",
        ""
    )


    # -------------------------
    # WHAT MATTERS
    # -------------------------

    salary_importance = request.form.get(
        "salary_importance",
        ""
    )

    job_opportunity_importance = request.form.get(
        "job_opportunity_importance",
        ""
    )

    job_security_importance = request.form.get(
        "job_security_importance",
        ""
    )

    career_growth_importance = request.form.get(
        "career_growth_importance",
        ""
    )

    interest_importance = request.form.get(
        "interest_importance",
        ""
    )

    work_life_balance_importance = request.form.get(
        "work_life_balance_importance",
        ""
    )

    respect_importance = request.form.get(
        "respect_importance",
        ""
    )


    # -------------------------
    # PREPARATION
    # -------------------------

    weekly_learning_hours = request.form.get(
        "weekly_learning_hours",
        ""
    )

    certificate = request.form.get(
        "certificate",
        ""
    )

    internship = request.form.get(
        "internship",
        ""
    )

    project = request.form.get(
        "project",
        ""
    )


    # -------------------------
    # FUTURE PLANS
    # -------------------------

    after_college = request.form.get(
        "after_college",
        ""
    )

    work_location = request.form.get(
        "work_location",
        ""
    )

    starting_salary = request.form.get(
        "starting_salary",
        ""
    )


    # -------------------------
    # EMPLOYEE DETAILS
    # -------------------------

    currently_working = request.form.get(
        "currently_working",
        ""
    )

    current_job = request.form.get(
        "current_job",
        ""
    )

    current_industry = request.form.get(
        "current_industry",
        ""
    )

    years_experience = request.form.get(
        "years_experience",
        ""
    )

    current_salary = request.form.get(
        "current_salary",
        ""
    )

    career_match = request.form.get(
        "career_match",
        ""
    )

    employee_career_change = request.form.get(
        "employee_career_change",
        ""
    )


    # -------------------------
    # SAVE DATA
    # -------------------------

    data = [
        name,
        phone,
        age,
        study_year,

        career,
        specialization,
        career_clarity,
        reasons,
        who_helped,

        salary_importance,
        job_opportunity_importance,
        job_security_importance,
        career_growth_importance,
        interest_importance,
        work_life_balance_importance,
        respect_importance,

        weekly_learning_hours,
        certificate,
        internship,
        project,

        after_college,
        work_location,
        starting_salary,

        currently_working,
        current_job,
        current_industry,
        years_experience,
        current_salary,
        career_match,
        employee_career_change
    ]


    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(data)


    # Redirect instead of showing the form again
    return redirect("/submitted")


@app.route("/submitted")
def submitted():

    return render_template("submitted.html")


if __name__ == "__main__":

    create_csv()

    app.run(debug=True)