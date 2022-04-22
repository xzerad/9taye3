import configparser
from elasticsearch import Elasticsearch

config = configparser.ConfigParser()
config.read(r"C:\Users\Radwan\PycharmProjects\fastApiProject\utils\example.ini")


class ElasticSingleton:
    client = Elasticsearch(
                cloud_id=config["ELASTIC"]["cloud_id"],
                http_auth=(config["ELASTIC"]["user"], config["ELASTIC"]["password"]),
                request_timeout=1000,
            )

    @staticmethod
    def get_instance():
        return ElasticSingleton.client

