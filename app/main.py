from fastapi import FastAPI
from dotenv import load_dotenv

from .models import model

load_dotenv()

app = FastAPI()


app.include_router(model.model)
