# FastAPI sample project

## Requirements
Python 3.12

## Usage
To install and run the server, please execute the following from the root directory:

```
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev .\main.py
```

and open your browser to here:

```
http://localhost:8000/
```

Your OpenAPI definition lives here:

```
http://localhost:8000/docs