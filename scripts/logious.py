from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from brain import get_res
from chat import get_res_chat, clear_memory
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse


# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (you can specify specific origins)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow the specified HTTP methods
    allow_headers=["*"],  # Allow any headers
)

# Define request and response models
class InputData(BaseModel):
    text: str
    userID: str
    type: str
    img: str

class INPD(BaseModel):
    userID: str

class OutputData(BaseModel):
    response: str

# Your AI model goes here
def your_ai_model(input_text,userid,img):
    # Replace this with your actual AI model logic
    if img=="null":
        response_text = get_res(input_text,userid)
        return response_text
    else:
        return "Please switch to Chat mode of Ai for using the Img feature"

def your_ai_model2(input_text,userid,img):
    # Replace this with your actual AI model logic
    response_text = get_res_chat(input_text,userid,img)
    return response_text
# Define endpoint for interacting with the AI model
@app.post("/predict/", response_model=OutputData)
async def predict(input_data: InputData):
    input_text = input_data.text
    userid = input_data.userID
    type_ai = input_data.type
    img = input_data.img
    print(img)
    try:
        if type_ai=="Assistant":
            response_text = your_ai_model(input_text,userid,img)
            return {"response": response_text}
        elif type_ai=="Chat":
            response_text = your_ai_model2(input_text, userid,img)
            return {"response": response_text}
        else:
            return  {"respone": "Give A Correct Ai Type"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the file to the desired location or process it
        # For example, you can save it using 'file.filename' and 'file.read()'
        with open(f'./DATA/{file.filename}', "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/clear")
async def clear(input_data: INPD):
    userid = input_data.userID
    try:
        z = clear_memory(userid)
        return {"response": z}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))