import sys
from harmony import auth
from harmony import client as harmony_client

def login_to_logitech(email, password, harmony_ip, harmony_port=5222):
    """Logs in to the Logitech service.

    Args:
    args: argparse arguments needed to login.

    Returns:
    Session token that can be used to log in to the Harmony device.
    """
    token = auth.login(email, password)
    if not token:
        sys.exit('Could not get token from Logitech server.')

    session_token = auth.swap_auth_token(
        harmony_ip, harmony_port, token)
    if not session_token:
        sys.exit('Could not swap login token for session token.')

    return session_token

def get_client(ip, session_token, port=5222):
    return harmony_client.create_and_connect_client(
        ip, port, session_token)

#def set_activity(session_token):
#    client = harmony_client.create_and_connect_client(
#        harmony_ip, harmony_port, session_token)


#def create_client():
#    client.disconnect(send_close=True)
