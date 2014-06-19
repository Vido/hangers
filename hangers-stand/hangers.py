import json
import urllib2


class Hanger(object):

    def __init__(self, stand, location):
        self.stand = stand
        self.location = location
        self.status = False
        self.code = None
        self.pin = None

    def update(self, code):
        self.code = code
        self.url = stand.url + str(code)

    def refresh(self):
        response = urllib2.urlopen(self.url)
        stock_status = json.load(response)

        if stock_status[unicode(self.code)] >= 0:
            self.state = True
            pin.high()
        else:
            self.state = False
            pin.low()

    def status(self):
        return self.state


class Stand(object):

    def __init__(self):
        with open('config.json', 'r') as fp:
            self.config = json.load(fp)

        self.url = self.config['ws_url']
        self.hangers = []

    def _hang_hangers(self, board):
        self._board = board
        pin_list = self.config['pins']
        for location, pin in enumerate(pin_list):
            hanger = Hanger(self, location)
            hanger.pin = self._board.pins[pin]
            self.hangers.append(hanger)

    def refresh(self):
        for hanger in self.hangers:
            hanger.refresh()

    def list(self):
        hanger_list = []
        for hanger in self.hangers:
            hanger_list.append({
                'location': hanger.location,
                'code': hanger.code,
                'state': hanger.status,
            })

        return hanger_list
