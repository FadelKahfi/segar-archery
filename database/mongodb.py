import os

from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from requests.sessions import Request

# Load .env
load_dotenv()

# .env Variable
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_client():
    # URI ke Atlas
    atlas_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}{DB_HOST}"

    # Coba Atlas dulu
    try:
        client = MongoClient(atlas_uri, server_api=ServerApi("1"))
        client.admin.command("ping")  # test koneksi
        return client
    except Exception as e:
        print(f"Gagal connect Atlas: {e}")


# Client aktif
client = get_client()


# Database
def use_db():
    return client["SegarArcheryDB"]