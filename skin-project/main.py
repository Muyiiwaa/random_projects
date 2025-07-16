from fastapi import FastAPI,UploadFile,status,HTTPException,File
from pydantic import BaseModel
import logfire
import uvicorn
from schema import HomeResponse
from pathlib import Path
import shutil
from fastapi.responses import StreamingResponse



app = FastAPI(
    title= "Skin Condition Classifier",
    description="""This app contains the endpoints 
    for a machine learning model for predicting skin conditions.
    The endpoints generally accepts image of user's skin and check
    whether they are suffering from one of the following skin conditions:
    """,
    version= "v1"
)

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occured while processing the image")
    finally:
        temp_file.unlink(missing_ok=True)
    




if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4500, reload=True)
