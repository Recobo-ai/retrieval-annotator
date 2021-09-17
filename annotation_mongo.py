from os import error
import pymongo


class MongoAnnotation:
    def __init__(self, credentials, mongo_config):
        self.get_mongo_client(mongo_config, credentials)

    def get_mongo_client(self, config, credentials):
        mongo_collection = None
        mongo_client = pymongo.MongoClient(
            config["mongo_connect_url"].format(
                credentials["mongo_username"],
                credentials["mongo_password"],
                config["mongo_db"],
            )
        )
        mongo_db = mongo_client[config["mongo_db"]]
        mongo_collection = mongo_db[config["mongo_collection"]]
        try:
            mongo_client = pymongo.MongoClient(
                config["mongo_connect_url"].format(
                    credentials["mongo_username"],
                    credentials["mongo_password"],
                    config["mongo_db"],
                )
            )
            mongo_db = mongo_client[config["mongo_db"]]
            mongo_collection = mongo_db[config["mongo_collection"]]
            print("connected...")
        except:
            print("erorr connecting...")

        self.mongo_collection = mongo_collection

    def write_to_mongo(self, data):
        """ "
        dump content to mongo
        """
        response = None
        try:
            response = self.mongo_collection.insert_one(data)
            response = f"annotation saved with id {str(response.inserted_id)}"
        except Exception as e:
            print(e)
            response = "error while saving annotation"
        return response

    def get_page_number(self, annotator_name, annotator, col):
        """
        Get page number for the annotator
        """
        response = 0
        try:
            response = self.mongo_collection.find_one(
                sort=[(col, pymongo.DESCENDING)],
                filter={annotator: annotator_name},
            )[col]
        except Exception as e:
            print(e)
            print("error while getting page number")
        return response
