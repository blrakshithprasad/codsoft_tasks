# CODSOFT Backend Task 1 — Student Record Management API

Built from the requirements in the supplied CodSoft Backend Development brief.

## Implemented
- Flask REST backend
- Relational SQLite models: Students, Courses, Enrollments
- CRUD for students
- CRUD for courses
- Create/list/get/delete enrollments
- Input validation
- Duplicate protection
- Search, filtering, sorting and pagination
- HTTP status codes and JSON errors
- Modular models/routes/utils
- OpenAPI endpoint summary
- Pytest API test

## Run
```bash
python -m venv .venv
# activate the environment
pip install -r requirements.txt
python run.py
```

API base: `http://localhost:5000`

Example:
```bash
curl -X POST http://localhost:5000/api/students   -H "Content-Type: application/json"   -d '{"name":"Asha","email":"asha@example.com","age":21,"department":"CSE"}'
```

## Test
```bash
pytest -q
```
