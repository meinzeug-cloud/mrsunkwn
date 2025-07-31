from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from endpoints.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
@app.get("/api/status")
async def get_status():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/api/data")
async def get_data():
    # TODO: Implement data endpoint
    return {"data": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)