from fastapi import FastAPI,UploadFile,status,HTTPException
from pydantic import BaseModel
import logfire
import uvicorn
from schema import HomeResponse



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

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4500, reload=True)
