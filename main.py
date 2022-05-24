import json

from fastapi import FastAPI
from deta import Deta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

deta = Deta("a0yajbef_9suuW9RaRuF56dhpH8P4ua7mvquRWbht")

euro = deta.Base("euro")

origins = [
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/euro")
async def ShowEuroData():
    return euro.fetch()


@app.get("/")
async def ShowEuroData():
    # drive = deta.Drive("ui")
    # drive.put("main", r"C:\Users\ablaz\source\repos\PriceCompare\projekt-webscrapper\webscrapper-ui\index.html")

    return "Main test"


@app.get("/products")
async def ShowEuroData():
    return "Witam wszytkich bardzo serdecznie"
