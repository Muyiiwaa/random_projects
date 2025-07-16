from fastapi import FastAPI,UploadFile,status,HTTPException,File
from pydantic import BaseModel
import logfire
import uvicorn
from schema import HomeResponse,ModelResponse
from pathlib import Path
import shutil
from fastapi.responses import StreamingResponse
from utils import predict_image
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI(
    title= "Skin Condition Classifier",
    description="""This app contains the endpoints 
    for a machine learning model for predicting skin conditions.
    The endpoints generally accepts image of user's skin and check
    whether they are suffering from one of the following skin conditions:
    """,
    version= "v1"
)

logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))
logfire.instrument_fastapi(app)

# create home endpoint

@app.get("/",tags=["Home"], response_model=HomeResponse)
def root():
    """This is the root endpoint which serves as the base
    of the application. The initial call to the app url
    triggers this. The only thing this endpoint does is to
    serve as the entrypoint of the whole application.
    """
    return HomeResponse(message="we are live")


@app.post(path="/display_image/", tags = ["Images"])
def display_image(image_file: UploadFile = File(...)):
    """This endpoint accepts an image file and displays it 
    to the user.
    """
    try:
        temp_file = Path(f'temp_{image_file.filename}')
        # write the image to a new object
        with temp_file.open(mode="wb") as temp_buffer:
            shutil.copyfileobj(fsrc=image_file.file, fdst=temp_buffer)
        
        return StreamingResponse(content = open(temp_file, mode="rb"), media_type="image/png")
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occured while processing the image: {err}")
    finally:
        temp_file.unlink(missing_ok=True)
    

@app.post(path="/diagnose/", response_model=ModelResponse,tags=["diagnostics"])
def diagnose(image_file: UploadFile = File(...)):
    """
    This endpoint serves the skin condition diagnosis AI model
    that accepts an image of any skin condition between the 
    following ['Boil','clear skin','Eczema','keloids','Vitiligo']
    and returns a dignosis and the corresponding confidence of
    that diagnosis.
    """
    try:
        temp_file = Path(f'temp_{image_file.filename}')

        with temp_file.open(mode="wb") as buffer:
            shutil.copyfileobj(fsrc = image_file.file, fdst = buffer)
        
        probability, condition = predict_image(image_path = temp_file)
        logfire.info(f"""image_file: {image_file.filename},
        confidence: {round(probability, 3)},diagnosis: {condition}""")
        temp_file.unlink(missing_ok=True)
        
    except Exception as err:
        logfire.error(f"an error occured: {err}")
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"An error occured: {err}")
    
    return ModelResponse(predicted_condition = condition, confidence = round(probability, 3))
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4501, reload=True)
