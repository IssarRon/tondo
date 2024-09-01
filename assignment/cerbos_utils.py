import logging
import requests
from .user_roles import user_roles_map

# Set up the logger for this module
logger = logging.getLogger(__name__)

def check_permission(userid, action):
    # Get roles for the given user ID
    roles = user_roles_map.get(userid, [])
    logger.info(f"Checking permission for user {userid} with roles {roles} to perform {action}")

    payload = {
        "principal": {"roles": roles},
        "resource": {"kind": "transaction"},
        "action": action,
    }

    cerbos_url = "http://cerbos:3592/api/check"
    try:
        response = requests.post(cerbos_url, json=payload)
        logger.debug(f"Cerbos response: {response.status_code}, {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Cerbos: {e}")
        return False
