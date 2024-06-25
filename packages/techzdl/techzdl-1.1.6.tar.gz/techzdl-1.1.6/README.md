# TechZDL

A simple yet powerful file downloader package for Python.

## Description

TechZDL is a highly efficient and easy-to-use file downloader package for Python. It provides features for downloading files with multiple threads, dynamic worker adjustments based on network speed, and more.

## Installation

You can install TechZDL using pip:

```sh
pip install techzdl
```

To update TechZDL to the latest version, use:

```sh
pip install --upgrade techzdl
```

## Usage

Here's a basic example of how to use TechZDL:

### Basic Usage

> Code from [test.py](test.py) file

```python
import asyncio
from techzdl.api import TechZDL


async def main():
    techzdl = TechZDL()
    downloader = techzdl.get_downloader(url="https://link.testfile.org/bNYZFw")
    await downloader.start()


asyncio.run(main())
```

https://github.com/TechShreyash/techzdl/assets/82265247/33267e71-2b41-4dd1-b306-c87a197a3b57

## Configuration Parameters

The `get_downloader` method accepts several parameters to customize the download process:

- **url (str)**: URL of the file to download.

- **custom_headers (Optional[dict], optional)**: Custom headers to send with the request. Defaults to `None`.

- **output_dir (Union[str, Path], optional)**: Directory where the file will be saved. Defaults to `"downloads"`.

- **filename (Optional[str], optional)**: Name to save the file as (including extension). By default, this will be determined automatically based on the URL or Content-Disposition header.

- **workers (Optional[int], optional)**: Number of fixed concurrent download workers. By default, this will be dynamically adjusted based on the download speed. Setting this will disable dynamic worker adjustment.

- **initial_dynamic_workers (int, optional)**: Initial number of dynamic workers. Defaults to `2`.

- **dynamic_workers_update_interval (int, optional)**: Interval in seconds to update the dynamic worker count. Defaults to `5`.

- **debug (bool, optional)**: Enable debug logs. Defaults to `True`.

- **progress (bool, optional)**: Enable download progress display. Defaults to `True`.

- **progress_callback (Optional[Union[Callable[..., Any], Callable[..., Awaitable[Any]]]], optional)**:
  Callback function for download progress updates. Can be sync or async. Defaults to `None`. Setting this disables `tqdm` progress.

- **progress_args (tuple, optional)**: Additional arguments for `progress_callback`. Defaults to `()`.

- **progress_interval (int, optional)**: Time interval for progress updates in seconds. Defaults to `1`.

- **chunk_size (int, optional)**: Size of each download chunk in bytes. Defaults to `5 MB`.

- **single_threaded (bool, optional)**: Force single-threaded download. Defaults to `False`.

- **max_retries (int, optional)**: Maximum retries for each chunk/file download. Defaults to `3`.

- **timeout (int, optional)**: Timeout for each request in seconds. Defaults to `60`.

## Examples

Will be added soon

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
