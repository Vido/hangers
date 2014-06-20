import json
import urllib2


class Hanger(object):

    def __init__(self, stand, location):
        self.stand = stand
        self.location = location
        self.status = False
        self.code = None
        self.pin = None

    def configure(self, code):
        self.code = code
        self.url = self.stand.url + str(code)

    def refresh(self):
        response = urllib2.urlopen(self.url)
        stock_status = json.load(response)

        self.status = False
        if int(stock_status[unicode(self.code)]) > 0:
            self.status = True

    def update(self):
        if self.status:
            self.pin.high()
        else:
            self.pin.low()


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
            hanger.pin.mode = 'OUT'
            self.hangers.append(hanger)

    def refresh(self):
        for hanger in self.hangers:
            if hanger.code:
                hanger.refresh()
            hanger.update()

    def list(self):
        hanger_list = []
        for hanger in self.hangers:
            hanger_list.append({
                'location': hanger.location,
                'code': hanger.code,
                'state': hanger.status,
            })

        return hanger_list
