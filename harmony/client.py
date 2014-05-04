"""Client class for connecting to the Logitech Harmony."""

import json
import logging
import time

import sleekxmpp
from sleekxmpp.xmlstream import ET


LOGGER = logging.getLogger(__name__)


class HarmonyClient(sleekxmpp.ClientXMPP):
    """An XMPP client for connecting to the Logitech Harmony."""

    def __init__(self, auth_token):
        user = '%s@connect.logitech.com/gatorade.' % auth_token
        password = auth_token
        plugin_config = {
            # Enables PLAIN authentication which is off by default.
            'feature_mechanisms': {'unencrypted_plain': True},
        }
        super(HarmonyClient, self).__init__(
            user, password, plugin_config=plugin_config)

    def get_config(self):
        """Retrieves the Harmony device configuration.

        Returns:
          A nested dictionary containing activities, devices, etc.
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = (
            'vnd.logitech.harmony/vnd.logitech.harmony.engine?config')
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        assert action_cmd.attrib['errorcode'] == '200'
        device_list = action_cmd.text
        return json.loads(device_list)

    def get_current_activity(self):
        """Retrieves the current activity.

        Returns:
          A int with the activity ID.
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = (
            'vnd.logitech.harmony/vnd.logitech.harmony.engine?getCurrentActivity')
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        assert action_cmd.attrib['errorcode'] == '200'
        activity = action_cmd.text.split("=")
        return int(activity[1])

    def start_activity(self, activity_id):
        """Starts an activity.

        Args:
            activity_id: An int or string identifying the activity to start

        Returns:
          A nested dictionary containing activities, devices, etc.
        """
        iq_cmd = self.Iq()
        iq_cmd['type'] = 'get'
        action_cmd = ET.Element('oa')
        action_cmd.attrib['xmlns'] = 'connect.logitech.com'
        action_cmd.attrib['mime'] = ('harmony.engine?startactivity')
        cmd = 'activityId=' + str(activity_id) + ':timestamp=0'
        action_cmd.text = cmd
        iq_cmd.set_payload(action_cmd)
        result = iq_cmd.send(block=True)
        payload = result.get_payload()
        assert len(payload) == 1
        action_cmd = payload[0]
        return action_cmd.text

    def turn_off(self):
        """Turns the system off if it's on, otherwise it does nothing.

        Returns:
          True.
        """
        activity = self.get_current_activity()
        print activity
        if activity != -1:
            print "OFF"
            self.start_activity(-1)
        return True

def create_and_connect_client(ip_address, port, token):
    """Creates a Harmony client and initializes session.

    Args:
      ip_address: IP Address of the Harmony device.
      port: Port that the Harmony device is listening on.
      token: A string containing a session token.

    Returns:
      An instance of HarmonyClient that is connected.
    """
    client = HarmonyClient(token)
    client.connect(address=(ip_address, port),
                   use_tls=False, use_ssl=False)
    client.process(block=False)

    while not client.sessionstarted:
        time.sleep(0.1)

    return client
