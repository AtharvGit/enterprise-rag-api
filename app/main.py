from fastapi import FastAPI                                    #Python is the chef. FastAPI is the counter and the phone system.
from dotenv import load_dotenv
import os                                                      #explores interacts with computer 
load_dotenv()                                                  #connecting to .env file it loads environment variables from .env
from app.api.routes import router

app = FastAPI(title = os.getenv("PROJECT_NAME","Enterprise RAG API"), version = os.getenv("VERSION", "1.0.0"), description="A production-ready RAG API for securely querying corporate documents.")

app.include_router(router, prefix='/api/v1')


@app.get("/health")                                            #@ decorator have to go through this first 
async def health_check():
    #to verify api is running
    return {"miracle its running"}

