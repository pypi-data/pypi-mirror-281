# Posmo DataMarket SDK

This is a Python SDK for interacting with the Posmo DataMarket API.

## Usage

Install with pip:
```
pip install datamap.posmo_datamarket_sdk
```

Import Posmo DataMarket client:
```python
from datamap.posmo_datamarket_sdk import PosmoDataMarket
```

Initialize client:
```python
datamarket = PosmoDataMarket(project_code='project', username='username', password='password')
```

Optionally you can provide username and password in environment variables:
- Username: `POSMO_USERNAME`
- Password: `POSMO_PASSWORD`

### Client methods

#### query(*query*)

Executes provided SQL query and returns result.

```python
result = datamarket.query('SELECT * FROM moving;')
```

#### schema()

Opens database schema documentation in default browser.

```python
datamarket.schema()
```
