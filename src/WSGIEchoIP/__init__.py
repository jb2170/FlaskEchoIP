"""WSGI Echo IP"""

__version__ = "1.0.0"

from typing import Generator
from http import HTTPStatus
from wsgiref.types import WSGIEnvironment, StartResponse

class App:
    forwarded_ip_header_name = "X-Forwarded-For"

    def __init__(self, env: WSGIEnvironment, start_response: StartResponse) -> None:
        self.env = env
        self.start_response = start_response

    def __iter__(self):
        if self.ip is None:
            return self.do_502()

        return self.do_200()

    def get_header(self, header_name: str) -> str | None:
        return self.env.get(f"HTTP_{header_name.replace("-", "_").upper()}")

    @property
    def ip(self) -> str | None:
        return self.get_header(self.forwarded_ip_header_name)

    def do_respond(
        self,
        code: HTTPStatus,
        headers, body: bytes,
        content_type = "text/plain; charset=UTF-8"
    ) -> Generator[bytes, None, None]:
        response_line = f"{code} {code.phrase}"

        headers.append(("Content-Type", content_type))
        headers.append(("Content-Length", f"{len(body)}"))

        self.start_response(response_line, headers)

        yield body

    def do_502(self):
        code = HTTPStatus.BAD_GATEWAY
        headers = []
        body = f"Gateway didn't provide {self.forwarded_ip_header_name}\n".encode()

        return self.do_respond(code, headers, body)

    def do_200(self):
        code = HTTPStatus.OK
        headers = []
        body = b""

        body = f"{self.ip}\n".encode()

        return self.do_respond(code, headers, body)
