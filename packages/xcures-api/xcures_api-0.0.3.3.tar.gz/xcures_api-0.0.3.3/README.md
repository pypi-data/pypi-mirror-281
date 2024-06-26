# xcures_api ( only necessary api calls being implemented ATM)
python wrapper for the [xcures REST API](https://partner.xcures.com/api-docs).

## Status == UNSTABLEish
* The auth functionality is working.
* Subject API query is working, but not tested extensively.
* Other API hooks, ie: query, are not implemented in a trusted way quite yet.
* TODO: I'll benefit from a quick discussion w/the Xcures tech team.


# Installation

## Development
### Environment
#### Conda
* [Install Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/)
* Create a new environment.
```bash
conda create -y -n XCAPI -c conda-forge python=3.10 ipython pytest pip pytz requests ipython && conda activate XCAPI && pip install yaml_config_day twine
```

* Activate the environment
```bash
conda activate XCAPI
```

## Production // pip

### Install ( >> not yet registered with pypi <<)
```bash 
# pip install xcures_api
```

## Configuration

### YAML Credentials File
* Based on credentials obtained from xcures. Using the [yaml_config_day](https://github.com/Daylily-Informatics/yaml_config_day) package.
* Located in `~/.config/xcures/xcures_$XCURES_ENV.yaml`, where `XCURES_ENV=` might be `prod` or `test`.
* Contents:
  
```bash
export XCURES_ENV=prod
more ~/.config/xcures/xcures_$XCURES_ENV.yaml
```


```yaml
---
base_url: "https://partner.xcures.com"
base_auth_url: "https://xcures-patient-registry-prod.us.auth0.com"
project_id: "PROJECTIDHERE"
client_id: "CLIENTIDHERE"
client_secret: "SECRETKEYHERE"
```


# Usage
_given the env is set and the yaml file is configured_

## Authenticate
```python
from xcures.xcures_api import XCuresAPI as xc_api

# Initialize the API connection, using your credentials yaml file.
xc = xc_api()

# print the session id
print(xc)

# print your auth token
print(xc.token)

# print all subjects in the project
xc.subject()
```

# Tests
## Crude Dev Test
```python
conda activate XCAPI
python xcures_api/xcures_api.py # just for quick dev, this will be moved to proper pytest.
```

## Pytest
```bash
conda activate XCAPI
pytest
```
* This is one test checking if failure to find an appropriate yaml file will raise an exception. I'm not certain how much effort to put into mocking the REST api behavior given credentials are needed to use it. TODO: check with the xcures dev team to see if there are test credentials available.



# Update pypi
```bash
python setup.py sdist
twine upload --repository rcrf  dist/*
```