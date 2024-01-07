import json
import os
import time
import paho.mqtt.client as mqtt
import configparser



class SpaceApi(object):

    def __init__(self, config):
        self.status = dict(api = '0.13',
                  space = None,
                  logo = None,
                  url = None,
                  location = dict(
                      address = None,
                      lon = None,
                      lat = None),
                  feeds = dict(
                      calendar = dict(
                          type='ical',
                          url='https://kalender.eigenbaukombinat.de/public/public.ics'),
                      blog = dict(
                          type='rss',
                          url='https://eigenbaukombinat.de/index.xml'),
                      ),
                  contact = dict(
                      email = None,
                      ml = None),
                  state = dict(
                      icon = dict(
                          open = None,
                          closed = None),
                      open = False),
                  issue_report_channels = ['email'])
        self.status['space'] = config.get('space', 'space')
        self.status['logo'] = config.get('space', 'logo')
        self.status['url'] = config.get('space', 'url')
        self.status['location']['address'] = config.get('space', 'address')
        self.status['location']['lon'] = config.getfloat('space', 'lon')
        self.status['location']['lat'] = config.getfloat('space', 'lat')
        self.status['contact']['email'] = config.get('space', 'email')
        self.status['contact']['ml'] = config.get('space', 'ml')
        self.status['state']['icon']['open'] = config.get('space', 'open')
        self.status['state']['icon']['closed'] = config.get('space', 'closed')
        self.fn = config.get('space', 'filename')


    def open(self):
        self.status['state']['open'] = True 
        #self.status['state']['open'] = False 
        self.update()

    def close(self):
        self.status['state']['open'] = False
        self.update()

    def update(self):
        print('updating')
        with open('..', os.path.join('htdocs', self.fn), 'w') as out:
            json.dump(self.status, out)

#config_t21 = configparser.ConfigParser()
#config_t21.read('etc/spaceapi.ini')
config_ebk = configparser.ConfigParser()
config_ebk.read('etc/spaceapi_ebk.ini')

#T21 = SpaceApi(config_t21)
EBK = SpaceApi(config_ebk)


def get_last_pl():
    with open('.lastpl', 'r') as last_pl:
        return last_pl.read().strip()

def set_last_pl(pl):
    with open('.lastpl', 'w') as last_pl:
        last_pl.write(pl)

def mqtt_received(client, data, message):
    payload = message.payload.decode('utf8')
    if payload == get_last_pl():
        return
    if payload == 'true':
        #T21.open()
        EBK.open()
    elif payload == 'false':
        #T21.close()
        EBK.close()
    set_last_pl(payload)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected to mqtt")
        client.subscribe('space/status/open')
    else:
        print("Bad connection Returned code=",rc)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='EBK space api status')
    parser.add_argument('--mqtt_broker', dest='mqtt_broker', default='localhost', help='Hostname/IP of the mqtt server (default:localhost).')
    config = parser.parse_args()
    print(f"connecting to {config.mqtt_broker}")
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.connect(config.mqtt_broker)
    time.sleep(1)
    mqttc.on_message = mqtt_received
    mqttc.loop_start()
    while 1:
        pass
        time.sleep(1)

main()
