from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Union, Any

# Import modules
from modules.hello_world import hello_world_handler
from modules.index_vault import index_vault_handler
from modules.search_vault import search_vault_handler


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ObsidianRequest(BaseModel):
    action: str
    content: Union[str, List[Union[str, Dict[str, str]]]]

class ObsidianResponse(BaseModel):
    result: Any 

@app.get("/")
async def root():
    return {"message": "Hello from YourPal backend!"}

@app.post("/process")
async def process_request(request: ObsidianRequest) -> ObsidianResponse:
    if request.action == "hello_world":
        return ObsidianResponse(result=hello_world_handler(request.content))
    elif request.action == "index_vault":
        if isinstance(request.content, list) and len(request.content) == 2:
            return ObsidianResponse(result=index_vault_handler(request.content))
        else:
            raise HTTPException(status_code=400, detail="Invalid content format for index_vault action")
    elif request.action == "search_vault":
        if isinstance(request.content, list) and len(request.content) == 2:
            search_results = search_vault_handler(request.content)
            return ObsidianResponse(result=search_results)
        else:
            raise HTTPException(status_code=400, detail="Invalid content format for search_vault action")
    else:
        raise HTTPException(status_code=400, detail="Unknown action")

@app.get("/version")
async def version():
    return "1.0.0"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)