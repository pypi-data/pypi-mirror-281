# BlairWdq Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)
[![pypi](https://img.shields.io/pypi/v/blair-wdq)](https://pypi.python.org/pypi/blair-wdq)

The BlairWdq Python library provides convenient access to the BlairWdq API from Python.

## Installation

```sh
pip install blair-wdq
```

## Usage

Instantiate and use the client with the following:

```python
from blair-wdq.client import BlairWdqApi

client = BlairWdqApi()
client.perform_inference_on_speech_data(xi_api_key='xi-api-key', )
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
from blair-wdq.client import AsyncBlairWdqApi

client = AsyncBlairWdqApi()
await client.perform_inference_on_speech_data(xi_api_key='xi-api-key', )
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
