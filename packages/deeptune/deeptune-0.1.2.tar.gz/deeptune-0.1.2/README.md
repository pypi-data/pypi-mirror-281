# Deeptune234 Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)
[![pypi](https://img.shields.io/pypi/v/deeptune234)](https://pypi.python.org/pypi/deeptune234)

The Deeptune234 Python library provides convenient access to the Deeptune234 API from Python.

## Installation

```sh
pip install deeptune234
```

## Usage

Instantiate and use the client with the following:

```python
from deeptune234.client import Deeptune234Api

client = Deeptune234Api(
    xi_api_key="YOUR_XI_API_KEY",
)
client.perform_inference_on_speech_data(
    voice_id="voice_id",
    text="text",
)
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
from deeptune234.client import AsyncDeeptune234Api

client = AsyncDeeptune234Api(
    xi_api_key="YOUR_XI_API_KEY",
)
await client.perform_inference_on_speech_data(
    voice_id="voice_id",
    text="text",
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
