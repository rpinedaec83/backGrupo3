import os
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = 'mediagpr3'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = 'staticgpr3'
    expiration_secs = None