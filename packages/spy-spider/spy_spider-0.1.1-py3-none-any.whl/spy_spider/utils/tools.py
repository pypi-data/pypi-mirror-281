import httpx
import socket
from typing import Literal


def get_host(ip_type: Literal["local", "public"] = "local") -> str:
    if ip_type == "local":
        return socket.gethostbyname(socket.gethostname())
    elif ip_type == "public":
        return httpx.get("https://api.ipify.org").text
    else:
        raise ValueError("Unsupported ip_type!")
