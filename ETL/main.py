import configparser
import datetime
from itertools import chain
import re
from prefect import task, Flow
from prefect.executors.dask import LocalDaskExecutor
from extract import skymil, mytek, sbs
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from prefect.engine.results import LocalResult


@task(checkpoint=True, result=LocalResult(dir="./"))
def extract_skymil():
    return skymil.extract()


@task(checkpoint=True, result=LocalResult(dir="./"))
def extract_mytek():
    return mytek.extract()


@task(max_retries=3, retry_delay=datetime.timedelta(minutes=1), checkpoint=True, result=LocalResult(dir="./"))
def extract_sbs():
    return sbs.extract()


@task(checkpoint=True, result=LocalResult(dir="./"))
def reduce_fn(iterator_):
    return list(chain.from_iterable(iterator_))


@task(checkpoint=True, result=LocalResult(dir="./"))
def transform(docs):
    mask = re.compile(r"((?:\d|\.)+)")
    for doc in docs:
        regex = mask.search(doc["price"].replace(",", "."))
        doc["price"] = float(regex.group(1)) if regex else None

    return docs


@task()
def load(docs):
    config = configparser.ConfigParser()
    config.read("config.ini")
    client = Elasticsearch(
        cloud_id=config["ELASTIC"]["cloud_id"],
        http_auth=(config["ELASTIC"]["user"], config["ELASTIC"]["password"]),
        request_timeout=3000,
    )
    chunk_len = len(docs)//6
    print(chunk_len)
    bulk(
        client, [
            {
                "_index": "product",
                "_source": doc
            }
            for doc in docs
        ],
        chunk_size=chunk_len
    )


if __name__ == '__main__':
    with Flow("projet db") as f:
        skymil_products = extract_skymil()
        mytek_products = extract_mytek()
        sbs_products = extract_sbs()
        joined = reduce_fn([skymil_products, mytek_products, sbs_products])
        normalized = transform(joined)
        load(normalized)
    f.executor = LocalDaskExecutor()
    f.run()
