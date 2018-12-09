"""
Support for Phicomm DC1 switch.
Developer by NETYJ
version 1.0
"""

import logging
import datetime
import requests,json
import voluptuous as vol
import hashlib
import time

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME, CONF_MAC)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
_INTERVAL = 3

SCAN_INTERVAL = datetime.timedelta(seconds=_INTERVAL)
DEFAULT_NAME = 'dc1'
CONF_PORTS = 'ports'
DEFAULT_PATH = '/config/phicomm_token.txt'
CONF_PATH = 'tokenPath'

ATTR_STATE="switchstate"
ATTR_NAME="switchname"
ATTR_DEVICEID = "deviceid"
ATTR_P = "p"
ATTR_V = "v"
ATTR_TOTALELECT = "totalelect"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_MAC): cv.string,
    vol.Required(CONF_PORTS): dict,
    vol.Optional(CONF_PATH, default=DEFAULT_PATH): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Phicomm M1 sensor."""

    name = config.get(CONF_NAME)
    mac = config.get(CONF_MAC)
    ports = config.get(CONF_PORTS)
    tokenPath = config.get(CONF_PATH)
    
    devs = []
    portls = []
    i = 1
    for item1, item2 in ports.items():
        portls.append(PhicommDC1Port(hass,item2, i))
        i += 1

    devs.append(PhicommDC1Switch(hass, name, mac, portls, tokenPath))
    devs.append(portls[0])
    devs.append(portls[1])
    devs.append(portls[2])

    add_devices(devs)
    
class PhicommDC1Port(SwitchDevice):
    """Representation of a port of DC1 Smart Plug switch."""
    def __init__(self, hass, name,iport):
        """Initialize the switch."""
        self._hass = hass
        self._name = name
        self._iport = iport
        self.sw = None
        self._state = False
        self._state_attrs = {
            ATTR_STATE: False,
            ATTR_NAME: None,
        }
        
    @property
    def name(self):
        """Return the name of the Smart Plug, if any."""
        return self._name
        
    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs  
        
    @property
    def current_power_watt(self):
        """Return the current power usage in Watt."""
        #try:
        #    return float(self.data.current_consumption)
        #except ValueError:
        return None

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state_attrs[ATTR_STATE]

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        if self.sw == None:
            _LOGGER.debug('sw is none')
            return None
        elif self.sw._state == False:
            _LOGGER.debug('self st is false')
            return None            
        elif self.sw._state_attrs[ATTR_STATE] == False:
            _LOGGER.debug('sw ATTR_STATE is false')
            return None
            
        self._state_attrs[ATTR_STATE] = True
        self._state_attrs[ATTR_STATE] = self.sw.pressPlug(self._iport,True)
        _LOGGER.debug('after set, self._state_attrs[ATTR_STATE] is %s',self._state_attrs[ATTR_STATE])

    def turn_off(self):
        """Turn the switch off."""
        if self.sw == None:
            _LOGGER.debug('sw is none')
            return None
        elif self.sw._state == False:
            _LOGGER.debug('self st is false')
            return None            
        elif self.sw._state_attrs[ATTR_STATE] == False:
            _LOGGER.debug('sw ATTR_STATE is false')
            return None
            
        self._state_attrs[ATTR_STATE] = False
        self._state_attrs[ATTR_STATE] = self.sw.pressPlug(self._iport,False)
        _LOGGER.debug('after set, self._state_attrs[ATTR_STATE] is %s',self._state_attrs[ATTR_STATE])

    def setSwitch(self, switchDC1):   
        self.sw = switchDC1
        return None

class PhicommDC1Switch(SwitchDevice):
    """Representation of a DC1 Smart Plug switch."""

    def __init__(self, hass, name, mac, ports, tokenPath):
        """Initialize the switch."""
        self._hass = hass
        self._name = name
        self._mac = mac
        self._ports = ports
        self._ports[0].setSwitch(self)
        self._ports[1].setSwitch(self)
        self._ports[2].setSwitch(self)
        self._tokenPath = tokenPath
        self._state = False
        self.data = []
        self.fIsLogon = False
        self.access_token = None
        self.iCount = 0
        self.iWaitTime = 0
        self._state_attrs = {
            ATTR_STATE: False,
            ATTR_NAME: None,
            ATTR_DEVICEID: None,
            ATTR_P: None,
            ATTR_V: None,
            ATTR_TOTALELECT: None,
        }

    @property
    def name(self):
        """Return the name of the Smart Plug, if any."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs  

    @property
    def assumed_state(self):
        """Return true if unable to access real state of entity."""
        return False

    @property
    def should_poll(self):
        """Return the polling state."""
        return True
        
    @property
    def current_power_watt(self):
        """Return the current power usage in Watt."""
        #try:
        #    return float(self.data.current_consumption)
        #except ValueError:
        return None

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state_attrs[ATTR_STATE]

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        if self._state == False:
            return None
        self._state_attrs[ATTR_STATE] = True
        self._state_attrs[ATTR_STATE] = self.pressPlug(0,True)

    def turn_off(self):
        """Turn the switch off."""
        if self._state == False:
            return None
        self._state_attrs[ATTR_STATE] = False
        self._state_attrs[ATTR_STATE] = self.pressPlug(0,False)
            
    def pressPlug(self,iport,fOn):
        if self._state == False:
            return False

        try:
            m=hashlib.md5()
            m.update(bytes(str(time.time()),encoding='utf-8'))   
            headers2 = {'User-Agent': 'zhilian/5.7.0 (iPhone; iOS 10.0.2; Scale/3.00)',
                       'Authorization': self.access_token,
                       'Content-Type': 'application/json' }
            
            i = 0
            if self._ports[2]._state_attrs[ATTR_STATE] == True:
                i |= 0b1000
            if self._ports[1]._state_attrs[ATTR_STATE] == True:
                i |= 0b100
            if self._ports[0]._state_attrs[ATTR_STATE] == True:
                i |= 0b10
            if self._state_attrs[ATTR_STATE] == True:
                i |= 0b1
                
            if fOn == False:
                i &= ~(1 << iport)
            else:
                i |= 1 << iport
            strT = bin(int(i))
            _LOGGER.debug('strT:%s, i:%d',strT,i)   
            strT = strT[2:len(strT)]
            payload = '{"uuid":"'+ m.hexdigest()[0:20].lower() +'","params":{"status":'+ strT +'},"auth":"","action":"datapoint="}'         
            _LOGGER.debug('payload:%s',payload)      
            #payload = '{"uuid":"cW6o375ejq1516990422","params":{},"auth":"","action":"datapoint"}'         
            resp = requests.post('https://smartplug.phicomm.com/SmartPlugAppV1/plug/'+self._state_attrs[ATTR_DEVICEID]+'/command', data=payload, headers=headers2,timeout=3)
            if resp.status_code == 200:
                obj = resp.json() 
                error = obj['error']
                if int(error) == 0:
                    return fOn
                else:
                    _LOGGER.error("switch control return failed: return value:%s, payload:%s",obj,payload)
                    return not fOn
            else:
                _LOGGER.error("switch control failed: resp:%s, payload:%s",resp,payload)
                return not fOn
                
        except OSError as e:
            _LOGGER.error("OSError: %s",e)
            return not fOn

    def update(self):
        """Get the latest data from the smart plug and updates the states."""
        #_LOGGER.debug('self.iWaitTime:%s',self.iWaitTime)
        if self.iWaitTime > 0:
            self.iWaitTime -= _INTERVAL
        if self.iWaitTime > 0:
            return None
            
        if self.fIsLogon is False:
            self.iCount += 1
            if self.iCount < 4:
                return None

        self.iCount = 0
        if self.access_token is None or self.fIsLogon is False:
            with open(self._tokenPath, 'r') as f:
                self.access_token = f.read()

        if self.access_token is None:
            return None
            
        try:
    
            headers = {'User-Agent': 'zhilian/5.7.0 (iPhone; iOS 10.0.2; Scale/3.00)',
                       'Authorization': self.access_token }
    
            
            if  self._state_attrs[ATTR_DEVICEID] is None:
                payload = {'productID': '7'}
                resp = requests.get('https://phicloudsym.phicomm.com/device/getBindDevs', params=payload, headers=headers,timeout=3)
                if resp.status_code == 200:
                    obj = resp.json() 
                    error = obj['error']
                    if int(error) == 0:
                        self.fIsLogon = True
                        for DevsData in iter(obj['devs']):
                            if str(DevsData['attributes']['mac']).upper() == self._mac.upper():
                                self._state_attrs[ATTR_NAME] = str(DevsData['name'])
                                self._state_attrs[ATTR_DEVICEID] = str(DevsData['deviceID'])
                                break
                        _LOGGER.debug('Find switch name:%s, deviceid:%s, mac:%s',self._state_attrs[ATTR_NAME],self._state_attrs[ATTR_DEVICEID],self._mac)
                    else:
                        _LOGGER.error('Find switch error, %s, payload:%s',obj,payload)
                        self.fIsLogon = False
                        return None
                else:
                    _LOGGER.error('get deviceid error, %s, payload:%s',resp,payload)
                    self.fIsLogon = False
                    return None
    
            resp = requests.get('https://smartplug.phicomm.com/SmartPlugAppV1/plug/'+self._state_attrs[ATTR_DEVICEID]+'/online',headers=headers,timeout=3)
            if resp.status_code == 200:
                obj = resp.json() 
                error = obj['error']
                if int(error) == 0:
                    self.fIsLogon = True
                    if str(obj['detail']['onlineState']).upper() == 'FALSE':
                        self._state = False
                        self._ports[0]._state = False
                        self._ports[1]._state = False
                        self._ports[2]._state = False
                        self._state_attrs[ATTR_STATE] = False
                        self._ports[0]._state_attrs[ATTR_STATE] = False
                        self._ports[1]._state_attrs[ATTR_STATE] = False
                        self._ports[2]._state_attrs[ATTR_STATE] = False
                        self.iWaitTime = 30
                        _LOGGER.debug('switch offline retry in 30 seconds, deviceid:%s',self._state_attrs[ATTR_DEVICEID])
                        return None
                    else:
                        self._state = True   
                        self._ports[0]._state = True
                        self._ports[1]._state = True
                        self._ports[2]._state = True
                    #_LOGGER.debug('Find switch state is %s, deviceid:%s, server value:%s, obj:%s',self._state,self._state_attrs[ATTR_DEVICEID],obj['detail']['onlineState'],obj)
                else:
                    _LOGGER.error('get switch state error,deviceid:%s, %s',self._state_attrs[ATTR_DEVICEID], obj)
                    self.fIsLogon = False
                    return None
            else:
                _LOGGER.error('get deviceid state error, %d, deviceid:%s',resp,self._state_attrs[ATTR_DEVICEID])
                self.fIsLogon = False
                return None
                
            m=hashlib.md5()
            m.update(bytes(str(time.time()),encoding='utf-8'))   
            headers2 = {'User-Agent': 'zhilian/5.7.0 (iPhone; iOS 10.0.2; Scale/3.00)',
                       'Authorization': self.access_token,
                       'Content-Type': 'application/json' }
            payload = '{"uuid":"'+ m.hexdigest()[0:20].lower() +'","params":{},"auth":"","action":"datapoint"}'         
            #payload = '{"uuid":"cW6o375ejq1516990422","params":{},"auth":"","action":"datapoint"}'         
            resp = requests.post('https://smartplug.phicomm.com/SmartPlugAppV1/plug/'+self._state_attrs[ATTR_DEVICEID]+'/command', data=payload, headers=headers2,timeout=3)
            if resp.status_code == 200:
                obj = resp.json() 
                error = obj['error']
                if int(error) == 0:
                    self.fIsLogon = True
                    self._state_attrs.update({ATTR_P: str(obj['respData']['result']['P'])})
                    self._state_attrs.update({ATTR_V: str(obj['respData']['result']['V'])})
                    #obj['respData']['result']['I']
                    i = int(str(obj['respData']['result']['status']), base=2)
                    _LOGGER.debug('switch state i %d',i)
                    if i & 0b1 == 0:
                        self._state_attrs[ATTR_STATE] = False
                    else:
                        self._state_attrs[ATTR_STATE] = True
                    if i & 0b10 == 0 or self._state_attrs[ATTR_STATE] == False:
                        self._ports[0]._state_attrs[ATTR_STATE] = False
                    else:
                        self._ports[0]._state_attrs[ATTR_STATE] = True
                    if i & 0b100 == 0 or self._state_attrs[ATTR_STATE] == False:
                        self._ports[1]._state_attrs[ATTR_STATE] = False
                    else:
                        self._ports[1]._state_attrs[ATTR_STATE] = True
                    if i & 0b1000 == 0 or self._state_attrs[ATTR_STATE] == False:
                        self._ports[2]._state_attrs[ATTR_STATE] = False
                    else:
                        self._ports[2]._state_attrs[ATTR_STATE] = True
                    _LOGGER.debug('switch state is %s, 1:%s, 2:%s, 3:%s v:%sv, p:%sw',self._state_attrs[ATTR_STATE],self._ports[0]._state_attrs[ATTR_STATE],self._ports[1]._state_attrs[ATTR_STATE],self._ports[2]._state_attrs[ATTR_STATE],self._state_attrs[ATTR_V],self._state_attrs[ATTR_P])
                else:
                    _LOGGER.error('get switch plugs state error,deviceid:%s, %s, payload:%s',self._state_attrs[ATTR_DEVICEID], obj,payload)
                    self.fIsLogon = False
                    return None
            else:
                _LOGGER.error('get deviceid plugs state error, %d, deviceid:%s, payload:%s',resp,self._state_attrs[ATTR_DEVICEID],payload)
                self.fIsLogon = False
                return None
                
           
            resp = requests.get('https://smartplug.phicomm.com/SmartPlugAppV1/plug/'+self._state_attrs[ATTR_DEVICEID]+'/totalElect',headers=headers,timeout=3)
            if resp.status_code == 200:
                obj = resp.json() 
                error = obj['error']
                if int(error) == 0:
                    self._state_attrs.update({ATTR_TOTALELECT: obj['respData']['totalElect']})
                else:
                    _LOGGER.error('get switch totalElect error,deviceid:%s, %s',self._state_attrs[ATTR_DEVICEID], obj)
                    self.fIsLogon = False
                    return None
            else:
                _LOGGER.error('get deviceid totalElect error, %d, deviceid:%s',resp,self._state_attrs[ATTR_DEVICEID])
                self.fIsLogon = False
                return None
                
        except OSError as e:
            self.fIsLogon = False
            _LOGGER.error("OSError: %s",e)


