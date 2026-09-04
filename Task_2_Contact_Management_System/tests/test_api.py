import tempfile,os
from app import create_app
def test_contact_api():
    f=tempfile.NamedTemporaryFile(suffix=".db",delete=False);f.close()
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///"+f.name})
    with app.test_client() as c:
        r=c.post("/api/contacts",json={"name":"Ravi","email":"ravi@example.com","phone":"+919999999999","address":"Bengaluru","company":"ABC"})
        assert r.status_code==201
        cid=r.get_json()["id"]
        assert c.post("/api/contacts",json={"name":"Ravi 2","email":"ravi@example.com","phone":"+918888888888"}).status_code==409
        assert c.get("/api/contacts?q=ravi").status_code==200
        assert c.put(f"/api/contacts/{cid}",json={"name":"Ravi K","email":"ravi@example.com","phone":"+919999999999"}).status_code==200
        assert c.delete(f"/api/contacts/{cid}").status_code==200
    os.unlink(f.name)
