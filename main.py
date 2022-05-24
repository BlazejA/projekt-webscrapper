import json

import pymongo
from bson import json_util
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

client = pymongo.MongoClient("mongodb+srv://admin:admin1@atlascluster.5r0ou.mongodb.net/?retryWrites=true&w=majority")
db = client['apple_products']


@app.get("/euro")
async def ShowEuroData():
    table = db["euro_products"]
    data = list(parse_json(table.find({})))
    return data


@app.get("/")
async def ShowEuroData():
    return "Main test"


@app.get("/products")
async def ShowEuroData():
    return "Witam wszytkich bardzo serdecznie"


def parse_json(data):
    return json.loads(json_util.dumps(data))
