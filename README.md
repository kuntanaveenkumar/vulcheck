Test Project to Check Project Dependencies and vunerabilites using fastAPI.


Commands:

pip install -r requirements.txt

Curl command to create Project:

Endpoints:

curl -X POST http://localhost:8000/projects \
     -H "Content-Type: application/json" \
     -d '{"name": "My Project", "description": "Test project", "requirements": "fastapi==0.100.0\nhttpx==0.24.1"}'

http://127.0.0.1:8000/projects
http://127.0.0.1:8000/projects/<Projectid>/dependencies  (Renders Project based dependencies)
ex : http://127.0.0.1:8000/projects/1/dependencies 
http://127.0.0.1:8000/dependencies (All dependencies)
http://127.0.0.1:8000/dependencies/<dependencyname> 
ex: http://127.0.0.1:8000/dependencies/httpx

Running on local

uvicorn main:app --reload

Run Test cases:

pytest tests/test_main.py