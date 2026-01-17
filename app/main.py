from fastapi import FastAPI
from routers import users
from routers import projects
from routers import tasks

import uvicorn
# Create a FastAPI app instance
app = FastAPI()

@app.get("/", tags=["Trello App Health Check"])
async def root():
    return {"message": "Welcome to Trello Application"}

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
if __name__ == "__main__":
        uvicorn.run(
            "main:app",          # Module:App format
            host="0.0.0.0",      # Accessible from any network
            port=8000,           # Default port
            reload=True,         # Auto-reload on code changes (dev mode)
            log_level="info"     # Logging level
        )