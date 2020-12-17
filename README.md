# Asynchronous File Downloader

asyncdl is a simple wrapper around the aiohttp Python library. Its aim is to simplify the process of securely downloading files in Python applications.

### Features

In addition to just downloading files, it provides a couple basic but essential security features:
* SSRF protection: Prevents download requests from being executed on localhost or other private IP address spaces
* File-size restrictions: Limits the maximum filesize that will be downloaded, whether or not the server provides a valid Content-Length header

### Usage

The asyncdl module currently provides a single method for use: `download_file`

This method works by passing in a BufferedIOBase, be it an open BinaryIO file handler, or a BytesIO instance.

```python
import asyncio
import asyncdl

# Required only for Windows support
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

loop = asyncio.new_event_loop()
file = open('test.bin', 'wb+')
loop.run_until_complete(asyncdl.download_file('http://ipv4.download.thinkbroadband.com/10MB.zip', file, loop=loop,
                                              max_size=15 * 1024 * 1024))  # max_size is in bytes

```

### Exceptions

Should one of the provided security checks fail, the module will throw one of three exceptions.

A primary example is when a user attempts to execute a download request on localhost. An attack like this could expose
sensitive data on any server hosting a REST application (for example, ElasticSearch)
```python
import asyncio
import asyncdl

loop = asyncio.new_event_loop()
file = open('test.bin', 'wb+')
loop.run_until_complete(asyncdl.download_file('http://localhost:9200/_cat/indices', file, loop=loop,
                                              max_size=15 * 1024 * 1024))  # max_size is in bytes
```
In the above example, an `asyncdl.SecurityError` exception will be thrown.

If you try to download a file that exceeds the specified `max_size` parameter, an `asyncdl.FilesizeError` exception will be thrown.

If you either provide an invalid URL or `https_only` is enabled, and a non-secure link is provided, an `asyncdl.BadUrlError` exception will be thrown.