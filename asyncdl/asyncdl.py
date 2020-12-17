import asyncio
import io
import ipaddress
import os
import socket
import typing
from urllib.parse import urlparse

from aiodns import DNSResolver
from aiodns.error import DNSError
from aiohttp import ClientResponse, ClientSession

ERROR_MESSAGE_INSECURE_URL = 'An insecure URL was provided while https_only was enabled; refusing to proceed'
ERROR_MESSAGE_NO_HOSTNAME  = 'The specified URL is missing a hostname; unable to proceed'
ERROR_MESSAGE_DNS_FAILURE  = 'Failed to resolve the domains IP address; unable to proceed'


async def download_file(
        url: str,
        fh: typing.Union[io.BufferedIOBase, typing.BinaryIO],
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        ssrf_protection: bool = True,
        max_size: typing.Optional[int] = None,
        https_only: bool = False,
        keep_files_open: bool = False,
        **session_args
) -> io.BufferedIOBase:
    """
    Asynchronously downloads a file using the supplied BufferedIOBase
    Args:
        url: The file URL
        fh: Any valid BufferedIO instance. Generally either a writable file opened in binary mode, or a BytesIO instance
        loop: An active event loop to use. If not provided, a new one will be created.
        ssrf_protection: Server Side Request Forgery Protection: When enabled, the hostname is resolved prior to making
            an HTTP request to ensure that the provided hostname does not resolve to a private IP address space.
        max_size: The maximum filesize allowed in bytes. If the server returns a content size greater than this limit,
            or tries to send us more content than the server advertises, the download will be rejected.
        https_only: When true, non-secure download requests will be rejected.
        keep_files_open: Default behavior is to seek to the beginning and return an open file-handler for BytesIO
            instances while returning a closed file-handler for everything else. Set this to True if you always want
            an open file handler returned regardless of the fh type.
        **session_args: Any additional kwargs are passed along to aiohttp.ClientSession()

    Returns:
        io.BufferedIOBase
    """
    # Make sure we have a valid event loop
    loop = loop or asyncio.new_event_loop()

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
        resolver = DNSResolver(loop=loop)

        # We perform DNS resolutions via the systems hosts file first if available
        try:
            res = await resolver.gethostbyname(parsed_url.hostname, socket.AF_INET)
        except DNSError:
            raise BadUrlError(ERROR_MESSAGE_DNS_FAILURE)

        for ip in res.addresses:
            ip = ipaddress.ip_address(ip)  # type: typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
            if ip.is_private:
                raise SecurityError(ip)

    # If we're still here, everything should be good. Let's ready the download request.
    async with ClientSession(loop=loop, raise_for_status=True, **session_args) as session:  # type: ClientSession
        async with session.get(url, read_until_eof=max_size is None) as response:  # type: ClientResponse
            if (response.content_length and max_size) and response.content_length > max_size:
                fh.close()
                if hasattr(fh, 'name'):
                    os.remove(fh.name)
                raise FilesizeError(response.content_length)

            bytes_read = 0
            async for data in response.content.iter_chunked(1024):
                # Filesize exceeded. Nuke the file and abort.
                if max_size and bytes_read > max_size:
                    fh.close()
                    if hasattr(fh, 'name'):
                        os.remove(fh.name)

                    raise FilesizeError(bytes_read)

                fh.write(data)
                bytes_read += 1024

    if isinstance(fh, io.BytesIO):
        fh.seek(0)
        return fh

    if not keep_files_open:
        fh.close()

    return fh


class BadUrlError(Exception):
    pass


class SecurityError(Exception):
    pass


class FilesizeError(Exception):
    pass
