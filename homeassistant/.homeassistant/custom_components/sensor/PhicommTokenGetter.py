"""
Support for Phicomm Token Getter plant sensor.
Developer by NETYJ
version 1.0
"""
import logging
import datetime
import requests,json
import voluptuous as vol
import hashlib

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME,)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv


_LOGGER = logging.getLogger(__name__)
_INTERVAL = 30

SCAN_INTERVAL = datetime.timedelta(seconds=_INTERVAL)
DEFAULT_NAME = 'Phicomm Token Getter'
DEFAULT_PATH = '/config/phicomm_token.txt'
CONF_ACCOUNT = 'phicommAccount'
CONF_PWD = 'phicommPassowrd'
CONF_PATH = 'tokenPath'

ATTR_TOKEN = 'token'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PATH, default=DEFAULT_PATH): cv.string,
    vol.Required(CONF_ACCOUNT): cv.string,
    vol.Required(CONF_PWD): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Phicomm Token sensor."""

    name = config.get(CONF_NAME)
    phicommAccount = config.get(CONF_ACCOUNT)
    phicommPassowrd = config.get(CONF_PWD)
    tokenPath = config.get(CONF_PATH)

    devs = []

    devs.append(PhicommTokenSensor(
        hass, name, phicommAccount, phicommPassowrd,tokenPath))

    add_devices(devs)


class PhicommTokenSensor(Entity):
    """Implementing the Phicomm Token Getter."""
    def __init__(self, hass, name,phicommAccount,phicommPassowrd,tokenPath):
        """Initialize the sensor."""
        #_LOGGER.warning("name:%s, account:%s, pass:%s",name, phicommAccount,phicommPassowrd)
        
        self._hass = hass
        self._name = name
        self._phicommAccount = phicommAccount
        self._phicommPassowrd = phicommPassowrd
        self._tokenPath = tokenPath
        self._state = None
        self.data = []
        self.fIsLogon = False
        self.retryCountDown = 0
        self.slowDownStep = 0
        self.access_token = None
        self.lastResponeMsg = ''
        self._state_attrs = {
            ATTR_TOKEN: None,
        }
        #self.update()
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.fIsLogon
    
    @property
    def state_attributes(self):
        """Return the state of the sensor."""
        return self._state_attrs
   
    def update(self):
        """
        Update current conditions.
        """
        if self._hass.states.is_state('input_boolean.phicomm_token_reset','on'):
            states_attrs = {
               'friendly_name':'重试',
               'icon':'mdi:lock-reset'
            }
            self._hass.states.set('input_boolean.phicomm_token_reset', 'off',states_attrs)
            self.slowDownStep = 0
            self.retryCountDown = 0
            _LOGGER.warning('reset login prcess!')
            
        if self.fIsLogon:
            
            headers = {'User-Agent': 'zhilian/5.7.0 (iPhone; iOS 10.0.2; Scale/3.00)',
                       'Authorization': self.access_token }
            control_resp = requests.get('https://accountsym.phicomm.com/v1/accountDetail', headers=headers,timeout=10)
            if control_resp.status_code == 200:
                control_obj = control_resp.json() 
                if int(control_obj['error']) != 0: 
                    self.fIsLogon = False
                    _LOGGER.warning('Phicomm sync account. Going to renew token!: %s', control_obj)                   
            else:
                 self.fIsLogon = False
                 _LOGGER.warning('Phicomm sync account. connecting error! Going to renew token!: %d', control_resp.status_code)                   
                       
        elif self.retryCountDown <= 0:
            if self.slowDownStep < 5:
                self.slowDownStep += 1
                md5 = hashlib.md5()
                md5.update(str(self._phicommPassowrd).encode("utf8"))
                payload = {'authorizationcode' : 'feixun.SH_1', 
                           'password' : md5.hexdigest().upper(),
                            'phonenumber' : self._phicommAccount}
                #_LOGGER.warning("payload:%s",payload)
                headers = {'User-Agent': 'zhilian/5.7.0 (iPhone; iOS 10.0.2; Scale/3.00)'}
                resp = requests.post('https://accountsym.phicomm.com/v1/login', headers=headers,params=payload,timeout=10)
                if resp.status_code == 200:
                    obj = resp.json() 
                    error = obj['error']
                    if int(error) == 0:
                        self.access_token = obj['access_token']
                        with open(self._tokenPath, 'w') as f:
                            f.write(self.access_token)
                        self._state_attrs = {
                            ATTR_TOKEN: 'please check'+self._tokenPath+'to review the token.',
                        }
                        _LOGGER.warning("access_token:%s",self.access_token)
                        self.fIsLogon = True
                        self.retryCountDown = 60
                        self.slowDownStep = 0
                        self.lastResponeMsg = '' 
                    elif int(error) == 8:
                        _LOGGER.error('account login error: ' + obj['error'] + obj['message'])
                        self.lastResponeMsg = obj['message']
                        self.slowDownStep += 100
                        states_attrs = {
                           'friendly_name':'重试. Last error: '+ self.lastResponeMsg,
                           'icon':'mdi:lock-reset'
                        }
                        self._hass.states.set('input_boolean.phicomm_m1_reset', 'off',states_attrs)
                    else:
                        self.lastResponeMsg = obj['message']
                        _LOGGER.error('account login error: ' + obj['error'] + obj['message'])
            else:
                states_attrs = {'friendly_name':'重试. Last error: '+ self.lastResponeMsg,
                                'icon':'mdi:lock-reset'
                }
                self._hass.states.set('input_boolean.phicomm_m1_reset', 'off',states_attrs)
        else:
            self.retryCountDown -= _INTERVAL
            #_LOGGER.error("retryCountDown:%d", self.retryCountDown)
            states_attrs = {
               'friendly_name':'重试. Last error: Logged on at other place!',
               'icon':'mdi:lock-reset'
            }
            self._hass.states.set('input_boolean.phicomm_token_reset', 'off',states_attrs)

