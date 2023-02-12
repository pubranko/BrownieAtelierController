import requests
import msal
from decouple import config
import logging
from pprint import pprint
from shared import settings
import json

app = msal.ConfidentialClientApplication(
    client_id=settings.AZURE_AD_CLIENT_ID,
    authority=settings.AZURE_AD_AUTHORITY,
    client_credential=settings.AZURE_AD_CLIENT_CREDENTIAL
)

scope = [settings.AZURE_FUNCTION_SCOPE]
result = None
result = app.acquire_token_silent(scope, account=None)

if not result:
    logging.info(
        "No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=scope)

print(f'結果:{result}\n==================\n')

headers = {'Authorization': 'Bearer {}'.format(result['access_token'])},

if "access_token" in result:
    response = requests.post(
        url=settings.AZURE_FUNCTION_URL,
        params={
            "code": settings.AZURE_FUNCTION_KEY,
        },
        data=json.dumps({
            # "target_container":settings.TARGET_CONTAINER__AUTO,
            # "target_container":settings.CONTAINER_APP__CONTAINER_GROUP_NAME,
            # "target_container":settings.CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL,
            "target_container":settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME,
            # "container_controll_command": settings.CONTAINER_CONTROLL__CREATE,
            # "container_controll_command": settings.CONTAINER_CONTROLL__START,
            # "container_controll_command": settings.CONTAINER_CONTROLL__RESTART,
            "container_controll_command": settings.CONTAINER_CONTROLL__STOP,
            # "container_controll_command": settings.CONTAINER_CONTROLL__DELETE,
        }),
        headers={'Authorization': 'Bearer ' + result['access_token']}, )

    print(response.status_code)
    print(str(response.text))
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))
