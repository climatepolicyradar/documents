import documents_router
import rds_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(documents_router.router)
app.include_router(rds_router.router)


@app.get("/")
async def root():
    return {"service": "Documents API"}
