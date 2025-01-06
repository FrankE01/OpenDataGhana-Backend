from fastapi import FastAPI
from api.v1.router import router

app = FastAPI(title="Open Data Ghana API", version="0.1.0")
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
