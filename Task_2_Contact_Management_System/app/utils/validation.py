import re
EMAIL=re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
def validate(data):
    e={}
    for field in ["name","email","phone"]:
        if not str(data.get(field,"")).strip(): e[field]="This field is required."
    if data.get("email") and not EMAIL.match(str(data["email"])):e["email"]="Invalid email."
    if data.get("phone") and not re.match(r"^[0-9+()\-\s]{7,30}$",str(data["phone"])):e["phone"]="Invalid phone."
    return e
