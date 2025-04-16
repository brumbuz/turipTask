from fastapi import FastAPI
from routers.get_all import router as get_all_router
from routers.create import router as create_router
from routers.get_one import router as get_one_router
from routers.update import router as update_router
from routers.delete import router as delete_router
import uvicorn
app = FastAPI()

app.include_router(get_all_router)
app.include_router(create_router)
app.include_router(get_one_router)
app.include_router(update_router)
app.include_router(delete_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)