import tempfile,os
from app import create_app
def test_auth_and_task_crud():
    f=tempfile.NamedTemporaryFile(suffix=".db",delete=False);f.close()
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///"+f.name,"JWT_SECRET_KEY":"test"})
    with app.test_client() as c:
        r=c.post("/api/auth/register",json={"username":"user1","password":"password123"})
        assert r.status_code==201; token=r.get_json()["access_token"];h={"Authorization":f"Bearer {token}"}
        r=c.post("/api/tasks",headers=h,json={"title":"Study","priority":"high","category":"college"})
        assert r.status_code==201;tid=r.get_json()["id"]
        assert c.patch(f"/api/tasks/{tid}/status",headers=h,json={"completed":True}).status_code==200
        assert c.get("/api/tasks?status=completed",headers=h).status_code==200
        assert c.delete(f"/api/tasks/{tid}",headers=h).status_code==200
    os.unlink(f.name)
