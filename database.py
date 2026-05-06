import json
import os

FILENAME = "data/blog_posts.json"

def load_data():
    """
    Loads a JSON file
    :return: blog_posts
    """
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as handle:
            return json.load(handle)

    return []  # or {} depending on your use case


def write_data( data):
    """ write into a JSON file
    :param data: data to write
    """
    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)

    with open(FILENAME, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)