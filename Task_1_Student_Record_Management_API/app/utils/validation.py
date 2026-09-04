import re
EMAIL_RE=re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
def validate_student(data):
    errors={}
    if not isinstance(data.get("name"),str) or not data.get("name","").strip(): errors["name"]="Name is required."
    if not EMAIL_RE.match(str(data.get("email",""))): errors["email"]="Valid email is required."
    if not isinstance(data.get("age"),int) or not 16 <= data.get("age",0) <= 100: errors["age"]="Age must be an integer from 16 to 100."
    if not isinstance(data.get("department"),str) or not data.get("department","").strip(): errors["department"]="Department is required."
    return errors
def validate_course(data):
    errors={}
    if not data.get("code"): errors["code"]="Course code is required."
    if not data.get("name"): errors["name"]="Course name is required."
    if not isinstance(data.get("credits"),int) or not 1 <= data.get("credits",0) <= 10: errors["credits"]="Credits must be 1-10."
    return errors
def validate_enrollment(data):
    errors={}
    if not isinstance(data.get("student_id"),int): errors["student_id"]="student_id must be an integer."
    if not isinstance(data.get("course_id"),int): errors["course_id"]="course_id must be an integer."
    if not data.get("semester"): errors["semester"]="Semester is required."
    return errors
