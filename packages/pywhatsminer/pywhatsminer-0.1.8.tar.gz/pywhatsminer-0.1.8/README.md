# PyWhatsminer
Unofficial python api-client for MicroBT Whatsminer ASICs
---
_Code adapted from a python file found in the Whatsminer Telegram group that is credited to `@passby`_


## Installation
Python 3.x is required. (NOTICE: This lib has not been published in PIP yet, commands below will not work)

```
pip install pywhatsminer
```


## Basic Usage
Instantiate a `WhatsminerAccessToken` for each ASIC that you want to access. Then make read-only or writeable API calls through `WhatsminerAPI`

Read-only information can be retrieved with just the ASIC's ip address:

```python
from pywhatsminer import Client

asic = Client(ip="192.168.0.117", port=4028, password="SatoshiAnonymoto123")

asic.Power.on()
```

Writeable `WhatsminerAccessToken` objs will renew themselves if they go past the API's 30min expiration.


### Managing multiple ASICs
You could define a whole server farm's worth of Whatsminer ASICs and manage them all in one script:

```python
from client import Client

asics = [
    Client(ip="192.168.0.117", port=4028, password="123"),
    Client(ip="192.168.0.118", port=4028, password="123"),
    Client(ip="192.168.0.119", port=4028, password="123")
]

for asic in asics:
    if asic.System.get_summary().temperature > 80:
        asic.Power.off(respbefore=True)
```


## API Documentation
It's very difficult to find any information about the Whatsminer API. This PDF documentation is slightly out of date but is the best source found so far:

[WhatsminerAPI-V2.0.5.pdf](docs/WhatsminerAPI-V2.0.5.pdf)


## Package distribution notes
_There are just notes to self for updating the pypi distribution_
* Update the release number in `setup.py` and commit to repo.
* Draft a new release in github using the same release number.
* Run `python setup.py sdist`
* Publish the distribution to pypi: `twine upload dist/*`

