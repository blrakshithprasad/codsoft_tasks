import tempfile,os
from app import create_app,db

def setup_app():
    f=tempfile.NamedTemporaryFile(suffix=".db",delete=False);f.close()
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///"+f.name})
    return app,f.name

def test_student_crud_and_validation():
    app,path=setup_app()
    with app.test_client() as c:
        r=c.post("/api/students",json={"name":"Asha","email":"asha@example.com","age":21,"department":"CSE"})
        assert r.status_code==201
        sid=r.get_json()["id"]
        assert c.get(f"/api/students/{sid}").status_code==200
        assert c.put(f"/api/students/{sid}",json={"name":"Asha R","email":"asha@example.com","age":22,"department":"CSE"}).status_code==200
        assert c.delete(f"/api/students/{sid}").status_code==200
        assert c.post("/api/students",json={"name":"","email":"bad","age":5,"department":""}).status_code==400
    os.unlink(path)
