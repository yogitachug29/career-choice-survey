from flask import Flask, request, render_template, redirect
import csv
import json
import os
import urllib.request

app = Flask(__name__)

GOOGLE_SHEETS_URL = os.environ.get("GOOGLE_SHEETS_URL", "").strip()
CSV_FILE = "career_data.csv"

# Order of columns matching the Google Sheet
HEADERS = [
    "Current Status",
    "Age",
    "Study Year",
    "Current Job",
    "Current Industry",
    "Years of Experience",
    "Current Salary",
    "Did Current Career Match Childhood/Student Choice",
    "Employee Career Change",
    "Career Change Reason",
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
    "Expected Starting Salary"
]


def save_local_backup(row):
    """Keep a local backup only if Google Sheets is unavailable."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(HEADERS)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow(row)


def send_to_google_sheets(payload):
    if not GOOGLE_SHEETS_URL:
        raise RuntimeError("GOOGLE_SHEETS_URL is not configured")

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GOOGLE_SHEETS_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as response:
        result = response.read().decode("utf-8")
        if response.status != 200:
            raise RuntimeError(f"Google Sheets returned HTTP {response.status}: {result}")

        try:
            result_data = json.loads(result)
            if result_data.get("status") != "success":
                raise RuntimeError(result_data.get("message", "Google Sheets rejected the submission"))
        except json.JSONDecodeError:
            # Apps Script may return a redirect/HTML response even after accepting the POST.
            pass


@app.route("/")
def home():
    return render_template("careerform.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Common Demographics
    current_status = request.form.get("current_status", "")
    age = request.form.get("age", "")

    # Working Professional fields (Filled only if Working Professional)
    current_job = request.form.get("current_job", "")
    current_industry = request.form.get("current_industry", "")
    years_experience = request.form.get("years_experience", "")
    current_salary = request.form.get("current_salary", "")
    career_match = request.form.get("career_match", "")
    employee_career_change = request.form.get("employee_career_change", "")
    career_change_reason = request.form.get("career_change_reason", "")

    # Student fields (Filled only if Student)
    study_year = request.form.get("study_year", "")
    career = request.form.get("career", "")
    specialization = request.form.get("specialization", "")
    career_clarity = request.form.get("career_clarity", "")
    reasons = ", ".join(request.form.getlist("reason"))
    who_helped = request.form.get("who_helped", "")

    salary_importance = request.form.get("salary_importance", "")
    job_opportunity_importance = request.form.get("job_opportunity_importance", "")
    job_security_importance = request.form.get("job_security_importance", "")
    career_growth_importance = request.form.get("career_growth_importance", "")
    interest_importance = request.form.get("interest_importance", "")
    work_life_balance_importance = request.form.get("work_life_balance_importance", "")
    respect_importance = request.form.get("respect_importance", "")

    weekly_learning_hours = request.form.get("weekly_learning_hours", "")
    certificate = request.form.get("certificate", "")
    internship = request.form.get("internship", "")
    project = request.form.get("project", "")

    after_college = request.form.get("after_college", "")
    work_location = request.form.get("work_location", "")
    starting_salary = request.form.get("starting_salary", "")

    row = [
        current_status,
        age,
        study_year,
        current_job,
        current_industry,
        years_experience,
        current_salary,
        career_match,
        employee_career_change,
        career_change_reason,
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
        starting_salary
    ]

    payload = dict(zip(HEADERS, row))

    try:
        send_to_google_sheets(payload)
    except Exception as error:
        print("Google Sheets save failed:", error)
        try:
            save_local_backup(row)
        except Exception as backup_error:
            print("Local backup also failed:", backup_error)

    return redirect("/submitted")


@app.route("/submitted")
def submitted():
    return render_template("submitted.html")


if __name__ == "__main__":
    app.run(debug=True)
