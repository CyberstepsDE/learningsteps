from fastapi import FastAPI
from dotenv import load_dotenv
from routers.journal_router import router as journal_router
import logging

load_dotenv()

# TODO: Setup basic console logging
# Hint: Use logging.basicConfig() with level=logging.INFO
# Steps:
# 1. Configure logging with basicConfig()
# 2. Set level to logging.INFO
# 3. Add console handler
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()]) 

# 4. Test by adding a log message when the app starts
logging.info("Application starting up")

app = FastAPI(title="LearningSteps API", description="A simple learning journal API for tracking daily work, struggles, and intentions")
app.include_router(journal_router)