import os
from typing import Union, Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    # return {"Hello": "World"}
    content = """
<body>
<p><strong>Download Profile</strong></p>
<form method="GET" id="downloadForm">
    <input type="hidden" name="dummy" value="placeholder">
    
    <div>
        <label for="dirName">Directory Name (profiles_type_1 or profiles_type_2):</label>
        <input type="text" id="dirName" name="dirName" required>
    </div>
    <br>
    <div>
        <label for="nlsa">NLSA (number):</label>
        <input type="text" id="nlsa" name="nlsa" required pattern="[0-9]+">
        <small> (Must be a number)</small>
    </div>
    <br>
    <button type="submit">Download Profile</button>
</form>
<hr>
<p><strong>Upload Profile</strong></p>
<form method="POST" id="uploadForm" enctype="multipart/form-data">
    <input type="hidden" name="dummy" value="placeholder">
    
    <div>
        <label for="dirName">Directory Name (profiles_type_1 or profiles_type_2):</label>
        <input type="text" id="dirName" name="dirName" required>
    </div>
    <br>
    <div>
        <label for="nlsa">NLSA (number):</label>
        <input type="text" id="nlsa" name="nlsa" required pattern="[0-9]+">
        <small> (Must be a number)</small>
    </div>
    <br>
    <div>
        <label for="fileInput">Select File to Upload:</label>
        <input type="file" id="fileInput" name="file" required>
    </div>
    <br>
    <button type="submit">Upload Profile</button>
</form>
<script>
    document.getElementById('downloadForm').addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the values from the input fields
        const dirNameValue = document.getElementById('dirName').value;
        const nlsaValue = document.getElementById('nlsa').value;

        // Construct the dynamic action URL
        const dynamicAction = `/dowloadFile/${dirNameValue}/${nlsaValue}`;

        // Set the form action and submit
        this.action = dynamicAction;
        this.submit();
    });
    document.getElementById('uploadForm').addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the values from the input fields
        const dirNameValue = document.getElementById('dirName').value;
        const nlsaValue = document.getElementById('nlsa').value;

        // Construct the dynamic action URL
        const dynamicAction = `/uploadFile/${dirNameValue}/${nlsaValue}`;

        // Set the form action and submit
        this.action = dynamicAction;
        this.submit();
    });
</script>
</body>
    """
    return HTMLResponse(content=content)


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/dowloadFile/{dir_name}/{nlsa}")
async def download_file(dir_name: str, nlsa: int):
    file_name = f"nlsa{nlsa}.json"
    file_path = os.path.join(dir_name, file_name)
    return FileResponse(
        path=file_path,
        media_type='application/octet-stream', # General-purpose binary data
        filename=file_name     # The name the user will see and save
    )

@app.post("/uploadFile/{dir_name}/{nlsa}")
async def create_upload_file(dir_name: str, nlsa: int, file: UploadFile):
    profiles_dir_list = ["profiles_type_1", "profiles_type_2"]
    if dir_name not in profiles_dir_list:
        raise HTTPException(status_code=500, detail=f'{dir_name} not in {profiles_dir_list}')
    file_path = os.path.join(dir_name, f"nlsa{nlsa}.json")
    try:
        contents = file.file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename} to {file_path}"}