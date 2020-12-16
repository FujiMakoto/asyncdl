import asyncio

from aiohttp import ClientSession
from aiodns import DNSResolver
from typing import *


async def download_file(
        url: str,
        filepath: str,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        ssrf_protection: bool = True,
        max_size: Optional[int] = None,
        https_only: bool = False,
        **session_arts
):
    """
    Asynchronously downloads a file to the specified filepath
    Args:
        url: The file URL
        filepath: The filepath to save to. This can be a directory or a full path including the filename and extension.
            If only a directory is provided, the filename will be whatever the server returns.
        loop: An active event loop to use. If not provided, a new one will be created.
        ssrf_protection: Server Side Request Forgery Protection: When enabled, the hostname is resolved prior to making
            an HTTP request to ensure that the provided hostname does not resolve to a private IP address space.
        max_size: The maximum filesize allowed in bytes. If the server returns a content size greater than this limit,
            or tries to send us more content than the server advertises, the download will be rejected.
        https_only: When true, non-secure download requests will be rejected.
        **session_arts: Any additional kwargs are passed along to aiohttp.ClientSession()

    Returns:

    """
    pass


async def download_bytesio(
        filepath: str,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        ssrf_protection: bool = True,
        max_size: Optional[int] = None,
        https_only: bool = False,
        **session_arts
):
    pass


async def _perform_request():
    pass
