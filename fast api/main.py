from typing import Optional

from fastapi import FastAPI
from utils.ElasticSingleton import ElasticSingleton
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(q: str, cat: Optional[str] = None, skip: Optional[str] = None):
    client = ElasticSingleton.get_instance()
    query: dict = {
        "bool": {
            "must": [
                {
                    "query_string": {
                        "query": q,
                        "fields": [
                            "title",
                            "description",
                            "brand"
                        ]
                    }},
                {
                    "match": {
                        "available": True
                    }
                }

            ],
        }
    }

    if cat:
        query["bool"]["must"].append({
            "match": {
                "category": cat
            }
        })
    res = client.search(index="product", query=query, from_=skip)
    return res
