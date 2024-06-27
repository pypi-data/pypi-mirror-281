# Power BI Admin API
[![PyPI Latest Release](https://img.shields.io/pypi/v/power-bi-api-admin.svg)](https://pypi.org/project/power-bi-api-admin/)

Use scorb functionalities in your python application.
## Instalation
```sh
pip install power-bi-api-admin
```

# Configuration
## Environment variables
To use power-bi-api-admin, you need to set two environment variables:
```dotenv
# ---DOTENV EXAMPLE---
PBI_TENANT_ID = #Your TENANT_ID
PBI_CLIENT_ID = #Your CLIENT_ID
PBI_SECRET = #Your SECRET
PBI_BASE_URL = "https://api.powerbi.com/v1.0/myorg/admin"
```

# Usage Example
You can use power-bi-api-admin in order to read registers.


## List registers
You can use get methods to list registers of system table. See the following example:
```python
from power_bi_api import PowerBiApp

# Instantiate PowerBiApp client object
client = PowerBiApp()

#Get the app controller
client_app = client.app

#Call the method thats return data from api
apps_data = client_app.get_apps().get("value")
```