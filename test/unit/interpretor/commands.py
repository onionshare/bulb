import collections
import datetime
import unittest

import stem
import stem.response
import stem.version

from stem.interpretor.commands import ControlInterpretor, _get_fingerprint

from test import mocking
from test.unit.interpretor import CONTROLLER

try:
  # added in python 3.3
  from unittest.mock import Mock
except ImportError:
  from mock import Mock

EXPECTED_EVENTS_RESPONSE = """\
\x1b[34mBW 15 25\x1b[0m
\x1b[34mBW 758 570\x1b[0m
\x1b[34mDEBUG connection_edge_process_relay_cell(): Got an extended cell! Yay.\x1b[0m
"""

EXPECTED_INFO_RESPONSE = """\
moria1 (9695DFC35FFEB861329B9F1AB04C46397020CE31)
\x1b[34;1maddress: \x1b[0m128.31.0.34:9101 (us)
\x1b[34;1mpublished: \x1b[0m05:52:05 05/05/2014
\x1b[34;1mos: \x1b[0mLinux
\x1b[34;1mversion: \x1b[0m0.2.5.3-alpha-dev
\x1b[34;1mflags: \x1b[0mAuthority, Fast, Guard, HSDir, Named, Running, Stable, V2Dir, Valid
\x1b[34;1mexit policy: \x1b[0mreject 1-65535
\x1b[34;1mcontact: \x1b[0m1024D/28988BF5 arma mit edu
"""

EXPECTED_GETCONF_RESPONSE = """\
\x1b[34;1mlog\x1b[0m\x1b[34m => notice stdout\x1b[0m
\x1b[34;1maddress\x1b[0m\x1b[34m => \x1b[0m
"""

FINGERPRINT = '9695DFC35FFEB861329B9F1AB04C46397020CE31'


class TestInterpretorCommands(unittest.TestCase):
  def test_get_fingerprint_for_ourselves(self):
    controller = Mock()

    controller.get_info.side_effect = lambda arg: {
      'fingerprint': FINGERPRINT,
    }[arg]

    self.assertEqual(FINGERPRINT, _get_fingerprint('', controller))

    controller.get_info.side_effect = stem.ControllerError
    self.assertRaises(ValueError, _get_fingerprint, '', controller)

  def test_get_fingerprint_for_fingerprint(self):
    self.assertEqual(FINGERPRINT, _get_fingerprint(FINGERPRINT, Mock()))

  def test_get_fingerprint_for_nickname(self):
    controller, descriptor = Mock(), Mock()
    descriptor.fingerprint = FINGERPRINT

    controller.get_network_status.side_effect = lambda arg: {
      'moria1': descriptor,
    }[arg]

    self.assertEqual(FINGERPRINT, _get_fingerprint('moria1', controller))

    controller.get_network_status.side_effect = stem.ControllerError
    self.assertRaises(ValueError, _get_fingerprint, 'moria1', controller)

  def test_get_fingerprint_for_address(self):
    controller = Mock()

    self.assertRaises(ValueError, _get_fingerprint, '127.0.0.1:-1', controller)
    self.assertRaises(ValueError, _get_fingerprint, '127.0.0.901:80', controller)

    descriptor = Mock()
    descriptor.address = '127.0.0.1'
    descriptor.or_port = 80
    descriptor.fingerprint = FINGERPRINT

    controller.get_network_statuses.return_value = [descriptor]

    self.assertEqual(FINGERPRINT, _get_fingerprint('127.0.0.1', controller))
    self.assertEqual(FINGERPRINT, _get_fingerprint('127.0.0.1:80', controller))
    self.assertRaises(ValueError, _get_fingerprint, '127.0.0.1:81', controller)
    self.assertRaises(ValueError, _get_fingerprint, '127.0.0.2', controller)

  def test_get_fingerprint_for_unrecognized_inputs(self):
    self.assertRaises(ValueError, _get_fingerprint, 'blarg!', Mock())

  def test_when_disconnected(self):
    controller = Mock()
    controller.is_alive.return_value = False

    interpretor = ControlInterpretor(controller)
    self.assertRaises(stem.SocketClosed, interpretor.run_command, '/help')

  def test_quit(self):
    interpretor = ControlInterpretor(CONTROLLER)
    self.assertRaises(stem.SocketClosed, interpretor.run_command, '/quit')
    self.assertRaises(stem.SocketClosed, interpretor.run_command, 'QUIT')

  def test_help(self):
    interpretor = ControlInterpretor(CONTROLLER)

    self.assertTrue('Interpretor commands include:' in interpretor.run_command('/help'))
    self.assertTrue('Queries the tor process for information.' in interpretor.run_command('/help GETINFO'))
    self.assertTrue('Queries the tor process for information.' in interpretor.run_command('/help GETINFO version'))

  def test_events(self):
    interpretor = ControlInterpretor(CONTROLLER)

    # no received events

    self.assertEqual('\n', interpretor.run_command('/events'))

    # with enqueued events

    event_contents = (
      '650 BW 15 25',
      '650 BW 758 570',
      '650 DEBUG connection_edge_process_relay_cell(): Got an extended cell! Yay.',
    )

    for content in event_contents:
      event = mocking.get_message(content)
      stem.response.convert('EVENT', event)
      interpretor.register_event(event)

    self.assertEqual(EXPECTED_EVENTS_RESPONSE, interpretor.run_command('/events'))

  def test_info(self):
    controller, server_desc, ns_desc = Mock(), Mock(), Mock()

    controller.get_microdescriptor.return_value = None
    controller.get_server_descriptor.return_value = server_desc
    controller.get_network_status.return_value = ns_desc

    controller.get_info.side_effect = lambda arg, _: {
      'ip-to-country/128.31.0.34': 'us',
    }[arg]

    ns_desc.address = '128.31.0.34'
    ns_desc.or_port = 9101
    ns_desc.published = datetime.datetime(2014, 5, 5, 5, 52, 5)
    ns_desc.nickname = 'moria1'
    ns_desc.flags = ['Authority', 'Fast', 'Guard', 'HSDir', 'Named', 'Running', 'Stable', 'V2Dir', 'Valid']

    server_desc.exit_policy.summary.return_value = 'reject 1-65535'
    server_desc.platform = 'Linux'
    server_desc.tor_version = stem.version.Version('0.2.5.3-alpha-dev')
    server_desc.contact = '1024D/28988BF5 arma mit edu'

    interpretor = ControlInterpretor(controller)
    self.assertEqual(EXPECTED_INFO_RESPONSE, interpretor.run_command('/info ' + FINGERPRINT))

  def test_unrecognized_interpretor_command(self):
    interpretor = ControlInterpretor(CONTROLLER)

    expected = "\x1b[1;31m'/unrecognized' isn't a recognized command\x1b[0m\n"
    self.assertEqual(expected, interpretor.run_command('/unrecognized'))

  def test_getinfo(self):
    controller, getinfo = Mock(), collections.OrderedDict()
    controller.get_info.return_value = getinfo

    interpretor = ControlInterpretor(controller)

    getinfo['version'] = '0.2.5.1-alpha-dev (git-245ecfff36c0cecc)'
    self.assertEqual('\x1b[34m0.2.5.1-alpha-dev (git-245ecfff36c0cecc)\x1b[0m', interpretor.run_command('GETINFO version'))
    controller.get_info.assert_called_with(['version'])

    getinfo['process/user'] = 'atagar'
    self.assertEqual('\x1b[34m0.2.5.1-alpha-dev (git-245ecfff36c0cecc)\natagar\x1b[0m', interpretor.run_command('getinfo version process/user'))
    controller.get_info.assert_called_with(['version', 'process/user'])

    controller.get_info.side_effect = stem.ControllerError('kaboom!')
    self.assertEqual('\x1b[1;31mkaboom!\x1b[0m', interpretor.run_command('getinfo process/user'))

  def test_getconf(self):
    controller, getconf = Mock(), collections.OrderedDict()
    controller.get_conf_map.return_value = getconf

    interpretor = ControlInterpretor(controller)

    getconf['log'] = ['notice stdout']
    getconf['address'] = ['']

    self.assertEqual(EXPECTED_GETCONF_RESPONSE, interpretor.run_command('GETCONF log address'))
    controller.get_conf_map.assert_called_with(['log', 'address'])

  def test_setconf(self):
    controller = Mock()
    interpretor = ControlInterpretor(controller)

    self.assertEqual('', interpretor.run_command('SETCONF ControlPort=9051'))
    controller.set_options.assert_called_with([('ControlPort', '9051')], False)

  def test_setevents(self):
    controller = Mock()
    interpretor = ControlInterpretor(controller)

    self.assertEqual('\x1b[34mListing for BW events\n\x1b[0m', interpretor.run_command('SETEVENTS BW'))
    controller.add_event_listener.assert_called_with(interpretor.register_event, 'BW')

  def test_raw_commands(self):
    controller = Mock()
    controller.msg.return_value = 'response'
    interpretor = ControlInterpretor(controller)

    self.assertEqual('\x1b[34mresponse\x1b[0m', interpretor.run_command('NEW_COMMAND spiffyness'))
    controller.msg.assert_called_with('NEW_COMMAND spiffyness')
