import json
import logging

import requests


class ApiCaller:
    class ApiResultNotOk(Exception):
        pass

    def __init__(self, server, test_connection=True, show_api_definition=True):
        self.server = server
        self.event_offset = 0
        if test_connection:
            self._print_api_version()
        if show_api_definition:
            logging.info("API definition:")
            logging.info(self.api_help_parser())

    def _print_api_version(self):
        r = self._call('version')
        logging.info("API version: {}".format(r))

    def _call(self, path, params={}):  # TODO handle errors
        r = requests.get("{url}/api/{path}?{params}".format(
            url=self.server.settings.url,
            path=path,
            params='&'.join(["{k}={v}".format(k=k, v=v) for k, v in params.items()])
        ))
        parsed = json.loads(r.text)
        if not r.ok:
            raise self.ApiResultNotOk('Request returned {code}'.format(code=r.status_code))
        if parsed['result'] != 'ok':
            raise self.ApiResultNotOk('Request result was {result}'.format(result=parsed['result']))
        return parsed.get('response', None)

    def get_lists(self):
        return self._call('list/all')

    def get_status(self, attributes=True, members=True, participants=True):
        params = {
            'attributes': int(attributes),
            'members': int(members),
            'participants': int(participants)
        }
        return self._call("session/status", params)

    def reset_event_offset(self):
        result = self._call("log/range", {'count': 1, 'offset': -1})
        if result['events']:
            self.event_offset = result['events'][0]['index'] + 1
        else:
            self.event_offset = 0

    def get_new_events(self, offset=None):
        if offset is not None:
            self.event_offset = offset
        result = self._call("log/range", {'count': 100, 'offset': self.event_offset})
        if result['events']:
            self.event_offset = result['events'][-1]['index'] + 1
        return result['events']

    def send_chat(self, message, player_refid=None):
        params = {'message': message}
        if player_refid is not None:
            params['refid'] = player_refid
        return self._call("session/send_chat", params)

    def api_help_parser(self):
        api_desc = self._call('help')
        methods = api_desc['methods']
        output = ''
        for method in methods:
            output += "{name}?{parameters} ({response_type}) {description}\n".format(
                name=method['name'],
                parameters='&'.join([parameter['name'] for parameter in method['parameters']]),
                response_type=method['responsetype'],
                description=method['description'],
            )
        return output