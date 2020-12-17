import asyncio
import socket
from urllib.parse import urlparse

from aiodns.error import DNSError
from aiohttp import ClientSession
from aiodns import DNSResolver
from typing import *


ERROR_MESSAGE_INSECURE_URL = 'An insecure URL was provided while https_only was enabled; refusing to proceed'
ERROR_MESSAGE_NO_HOSTNAME  = 'The specified URL is missing a hostname; unable to proceed'
ERROR_MESSAGE_DNS_FAILURE       = 'Failed to resolve the domains IP address; unable to proceed'


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
    # Make sure we have a valid schema
    if not url.lower().startswith(('https://', 'http://')):
        if https_only:
            url = 'https://' + url
        else:
            url = 'http://' + url

    # Make sure the domain is secure if https_only is set
    if https_only and not url.lower().startswith('https://'):
        raise BadUrlError(ERROR_MESSAGE_INSECURE_URL)

    # Parse the URL into components
    parsed_url = urlparse(url)
    if not parsed_url.hostname:
        raise BadUrlError(ERROR_MESSAGE_NO_HOSTNAME)

    # Pre-resolve the hostname if necessary
    if ssrf_protection:
        resolver = DNSResolver(loop)

        # We perform DNS resolutions via the systems hosts file first if available
        try:
            res = await resolver.gethostbyname(parsed_url.hostname, socket.AF_INET)
        except DNSError:
            raise BadUrlError(ERROR_MESSAGE_DNS_FAILURE)

        for ip in res.addresses:
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


class BadUrlError(Exception):
    pass


class FilesizeError(Exception):
    pass
