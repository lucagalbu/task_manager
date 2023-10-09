from fastapi import FastAPI


def startServer():
    """Launched with `poetry run start_server` at root level"""
    
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


app = FastAPI()
