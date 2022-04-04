from fastapi import FastAPI

# Create the FastAPI instance
app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
