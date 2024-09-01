import logging
import requests
from .user_roles import user_roles_map

# Set up the logger for this module
logger = logging.getLogger(__name__)

def check_permission(userid, action):
    # Get roles for the given user ID
    roles = user_roles_map.get(userid, [])
    logger.info(f"Checking permission for user {userid} with roles {roles} to perform {action}")
    
    # Payload structure based on your policy file
    payload = {
        "principal": {
            "id": userid,
            "roles": roles
        },
        "resource": {
            "kind": "transaction",
            "instances": {
                "some-resource-id": {}
            }
        },
        "actions": [action]
    }

    logger.debug(f"Payload sent to Cerbos: {payload}")
    
    cerbos_url = "http://cerbos:3592/api/check"
    try:
        response = requests.post(cerbos_url, json=payload)
        logger.debug(f"Cerbos response: {response.status_code}, {response.text}")
        if response.status_code == 200:
            result = response.json()
            # Check the permission for the given action
            allowed = result.get('resourceInstances', {}).get('some-resource-id', {}).get('actions', {}).get(action) == 'EFFECT_ALLOW'
            return allowed
        else:
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Cerbos: {e}")
        return False
