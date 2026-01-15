from fastapi import FastAPI, Depends
from dotenv import load_dotenv 
# 1. uv sync                (if you have recently deleted .env folder)
# 2. uv add python-dotenv
# 3. uv add python-env
# 4. uv pip show python-dotenv
# 5. Ctrl + Shift + P -> Python Select Interpreter -> Enter path to interpreter -> give path to .env subfolder inside your project.
import tempfile
import os

load_dotenv()

app = FastAPI()

# .env.local + .gitignore
# This looks for a file named .env in your root directory
GEMINI_AI_MODEL_API_KEY = os.getenv("GEMINI_AI_MODEL_API_KEY")   # 2. Call it to load variables from your .env file

# Now you can access variables
db_con_str = os.getenv("DATABASE_CONNECTION_STR")

def get_config():
    print("\n CONFIG FUNC: 1")
    return {"app": "task-api", "gemini_key":os.getenv("GEMINI_AI_MODEL_API_KEY")}

@app.get("/hello")
def hello(config: dict = Depends(get_config)):
    print("\n NORMAL API: 2")
    return {"message": "all good", "gemini_key": config["gemini_key"]}

# Dependency Injection
######################
# def get_temp_file():
#     """Provide a temporary file that gets cleaned up."""
#     # Setup: create the file
#     fd, path = tempfile.mkstemp()
#     file = os.fdopen(fd, 'w')   
#     try:
#         yield file  # Provide to endpoint
#     finally:
#         # Cleanup: runs after endpoint completes
#         file.close()
#         os.unlink(path)


# @app.post("/upload")
# def process_upload(temp = Depends(get_temp_file)):
#     temp.write("data")
#     return {"status": "processed"}
