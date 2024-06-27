# Embloy Python

Embloy's Python SDK for interacting with your Embloy integration.

## Usage

Install Embloy-Node SDK:

```Bash
# Install through pip
pip3 install --upgrade embloy_sdk
```

or in your requirements.txt
```python
# Find the version you want to pin:
# https://pypi.org/project/embloy-sdk/#history
# Specify that version in your requirements.txt file
embloy_sdk>=0.3.28
```

Integrate it in your service:

```Python
# In your application or script
from embloy_sdk import EmbloyClient, EmbloySession, SessionOptions

# Replace with your actual values
client_token = 'your_client_token'
options = SessionOptions('your_success_url', 'your_cancel_url')
session = EmbloySession("job", "your_job_slug", options)

# Make a request to the Embloy API
redirect_url = EmbloyClient(client_token, session).make_request()
```

## Run the tests
```Bash
python -m unittest tests/test_embloy_client.py
```

## Publish Package
```Bash

python setup.py sdist bdist_wheel

twine upload dist/*
```

---

© Carlo Bortolan, Jan Hummel

> Carlo Bortolan &nbsp;&middot;&nbsp;
> GitHub [@carlobortolan](https://github.com/carlobortolan) &nbsp;&middot;&nbsp;
> contact via [bortolanoffice@embloy.com](mailto:bortolanoffice@embloy.com)
>
> Jan Hummel &nbsp;&middot;&nbsp;
> GitHub [@github4touchdouble](https://github.com/github4touchdouble) &nbsp;&middot;&nbsp;
> contact via [hummeloffice@embloy.com](mailto:hummeloffice@embloy.com)

