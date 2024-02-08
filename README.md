# coldfront_storage_sync
A [ColdFront](https://coldfront.readthedocs.io/en/latest/) plugin that automatically adds and modifies storage shares according to Coldfront allocations
## Installation
If you're using a virtual environment (following ColdFront's deployment instructions should have you make and use a virtual environment), make sure you're in the virutal environment first.
```
pip install git+https://github.com/Ponyssimo/coldfront_storage_sync.git
```
## Configuration
Add the following to ColdFront's [local settings](https://coldfront.readthedocs.io/en/latest/config/#configuration-files):
```
INSTALLED_APPS += ["coldfront_plugin_storage_sync"]
```