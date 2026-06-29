from hashlib import blake2b
import os
from dotenv import load_dotenv
load_dotenv()


def hash_this(
        text: str,
        size: int | None = None,
        key: str | None = None):
    size = size or int(os.environ["HASH_SIZE"])
    key = key or os.environ["HASH_SIZE"]
    hs = blake2b(digest_size=size, key=key.encode("utf-8"))
    hs.update(text.encode("utf-8"))
    return hs.hexdigest()
