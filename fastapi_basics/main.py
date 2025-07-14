from fastapi import FastAPI
import uvicorn


# create an app instance
app = FastAPI(
    title= "My First API",
    summary= "This app contains endpoints for learning api basics",
    version= "v1")


# create our first endpoint.
@app.get(path='/')
def home():
    return {'message': 'Hello! welcome to the home page!!'}

@app.post(path='/converter/')
def convert_currency(base_currency: float, rate:float, 
                     final_currency: str):
    amount = base_currency * rate
    return {"base currency": {base_currency},
            "final currency": f"{amount} {final_currency}"}

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080, host="localhost", reload=True)
