import logging
import requests
from .consts import user_roles_map

# Initialize logger for this module
logger = logging.getLogger(__name__)

# URL to Cerbos API for permission checks
CERBOS_URL = "http://cerbos:3592/api/check"

#retrieve roles for a given user ID.
def get_user_roles(userid):
    roles = user_roles_map.get(userid, [])
    logger.info(f"Retrieved roles for user {userid}: {roles}")
    return roles

#build the payload to send to the Cerbos API for permission checking.
def build_cerbos_payload(userid, roles, action, resource_id):
    payload = {
        "principal": {
            "id": userid,
            "roles": roles
        },
        "resource": {
            "kind": "transaction", 
            "instances": {
                resource_id: {}
            }
        },
        "actions": [action]
    }
    logger.debug(f"Constructed Cerbos payload: {payload}")
    return payload

#send the permission check payload to the Cerbos API
def call_cerbos_api(payload):
    try:
        response = requests.post(CERBOS_URL, json=payload)
        response.raise_for_status()
        logger.debug(f"Cerbos API response: {response.status_code}, {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Cerbos: {e}")
        return None

#Check if a user has permission to perform a specific action on a resource.
def check_permission(userid, action, resource_id):
    roles = get_user_roles(userid)
    payload = build_cerbos_payload(userid, roles, action, resource_id)
    result = call_cerbos_api(payload)

    if result:
        allowed = result.get('resourceInstances', {}).get(str(resource_id), {}).get('actions', {}).get(action) == 'EFFECT_ALLOW'
        logger.info(f"Permission check result for user {userid}, action {action} on resource {resource_id}: {allowed}")
        return allowed
    else:
        return False
