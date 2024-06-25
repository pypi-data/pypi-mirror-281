import io

import asyncio

class HttpStreaming:
    """request method, e.g., GET, POST, etc."""
    method: str
    """request content type, e.g., application/json, text/html, etc."""
    content_type: str

    def stream(self, content_type: str) -> io.RawIOBase:
        """Returns a stream to write the response content.
          Args:
                content_type (str): the content type of the response.
        """
        raise NotImplementedError

class SansIOProtocol:
    """A protocol that does not use IO."""
    def process(self, data: bytes):
        """Processes the data."""
        raise NotImplementedError
