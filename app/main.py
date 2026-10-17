from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def get_hello() -> str:
    return 'Hello, world'
