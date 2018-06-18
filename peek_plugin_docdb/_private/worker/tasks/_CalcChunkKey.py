import logging

logger = logging.getLogger(__name__)


def makeChunkKey(modelSetKey: str, key: str) -> str:
    """ Make Chunk Key

    This is simple, and provides a reasonable distribution

    :param modelSetKey:
    :param key:

    :return: chunkKey

    """

    if not modelSetKey:
        raise Exception("modelSetKey is None or zero length")

    if not key:
        raise Exception("key is None or zero length")

    bucket = 0
    for char in key:
        bucket = ((bucket << 5) - bucket) + ord(char)
        bucket = bucket | 0  # This is in the javascript code.

    bucket = bucket & 1023  # 1024 buckets

    return '%s.%s' % (modelSetKey, bucket)
