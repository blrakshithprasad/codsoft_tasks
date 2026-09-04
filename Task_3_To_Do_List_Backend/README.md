# CODSOFT Backend Task 3 — To-Do List Backend

## Implemented
- REST CRUD for tasks
- SQLite relational storage
- JWT user authentication
- Password hashing
- Per-user task isolation
- Completed/pending status
- Search and filtering
- Pagination
- Validation
- Proper HTTP status codes
- Controllers/routes/models separation
- Due dates
- Priority levels
- Categories
- OpenAPI endpoint documentation
- Pytest test

Run:
```bash
pip install -r requirements.txt
python run.py
```

Register:
```bash
curl -X POST http://localhost:5000/api/auth/register -H "Content-Type: application/json" -d '{"username":"demo","password":"password123"}'
```
Use returned JWT as `Authorization: Bearer <token>`.

Test:
```bash
pytest -q
```
