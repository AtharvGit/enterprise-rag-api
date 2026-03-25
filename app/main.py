from fastapi import FastAPI                                    #Python is the chef. FastAPI is the counter and the phone system.
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os                                                      #explores interacts with computer 
load_dotenv()                                                  #connecting to .env file it loads environment variables from .env
from app.api.routes import router

app = FastAPI(title = os.getenv("PROJECT_NAME","Enterprise RAG API"), version = os.getenv("VERSION", "1.0.0"), description="A production-ready RAG API for securely querying corporate documents.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites (you can restrict this later)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, etc.
    allow_headers=["*"],
)

app.include_router(router, prefix='/api/v1')


@app.get("/health")                                            #@ decorator have to go through this first 
async def health_check():
    #to verify api is running
    return {"miracle its running"}

