import logging
from datetime import timedelta

# 此处引入了几个异步处理的库
import asyncio
import async_timeout
import aiohttp

import voluptuous as vol

# aiohttp_client将aiohttp的session与hass关联起来
# track_time_interval需要使用对应的异步的版本
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util


_LOGGER = logging.getLogger(__name__)

TIME_BETWEEN_UPDATES = timedelta(seconds=600)

CONF_OPTIONS = "options"
CONF_CITY = "city"
CONF_APPKEY = "appkey"

CONDITION_CLASSES = {
    'sunny': ["晴"],
    'cloudy': ["多云"],
    'partlycloudy': ["少云", "晴间多云", "阴"],
    'windy': ["有风", "微风", "和风", "清风"],
    'windy-variant': ["强风", "疾风", "大风", "烈风"],
    'hurricane': ["飓风", "龙卷风", "热带风暴", "狂暴风", "风暴"],
    'rainy': ["毛毛雨", "小雨", "中雨", "大雨", "极端降雨"],
    'pouring': ["暴雨", "大暴雨", "特大暴雨", "阵雨", "强阵雨"],
    'lightning-rainy': ["雷阵雨", "强雷阵雨"],
    'fog': ["雾", "薄雾"],
    'hail': ["雷阵雨伴有冰雹"],
    'snowy': ["小雪", "中雪", "大雪", "暴雪", "阵雪"],
    'snowy-rainy': ["雨夹雪", "雨雪天气", "阵雨夹雪"],
}

# 定义三个可选项：温度、湿度、PM2.5
OPTIONS = {
    "3hour": ["hourly_forcast_3", "未来3小时"],
    "6hour": ["hourly_forcast_6", "未来6小时"],
    "9hour": ["hourly_forcast_9", "未来9小时"],
    "12hour": ["hourly_forcast_12", "未来12小时"],
    "15hour": ["hourly_forcast_15", "未来15小时"],
    "18hour": ["hourly_forcast_18", "未来18小时"],
    "21hour": ["hourly_forcast_21", "未来21小时"],
    "24hour": ["hourly_forcast_24", "未来一天"],
}

ATTR_UPDATE_TIME = "更新时间"
ATTRIBUTION = "来自和风天气的天气数据"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CITY): cv.string,
    vol.Required(CONF_APPKEY): cv.string,
    vol.Required(CONF_OPTIONS,
                 default=[]): vol.All(cv.ensure_list, [vol.In(OPTIONS)]),
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """这个协程是程序的入口，其中add_devices函数也变成了异步版本."""
    _LOGGER.info("setup platform sensor.Heweather...")

    city = config.get(CONF_CITY)
    appkey = config.get(CONF_APPKEY)
    # 这里通过 data 实例化class weatherdata，并传入调用API所需信息
    data = WeatherData(hass, city, appkey)  
    # 调用data实例中的异步更新函数，yield 现在我简单的理解为将后面函数变成一个生成器，减小内存占用？
    yield from data.async_update(dt_util.now()) 
    async_track_time_interval(hass, data.async_update, TIME_BETWEEN_UPDATES)

    # 根据配置文件options中的内容，添加若干个设备
    dev = []
    for option in config[CONF_OPTIONS]:
        dev.append(HeweatherWeatherSensor(data, option))
    async_add_devices(dev, True)


class HeweatherWeatherSensor(Entity):
    """定义一个温度传感器的类，继承自HomeAssistant的Entity类."""

    def __init__(self, data, option):
        """初始化."""
        self._data = data
        self._object_id = OPTIONS[option][0]
        self._friendly_name = OPTIONS[option][1]
        self._icon = 'mdi:weather-'+'sunny'
        self._unit_of_measurement = TEMP_CELSIUS

        self._type = option
        self._state = None
        self._updatetime = None

    @property
    def name(self):
        """返回实体的名字."""
        return self._object_id

    @property
    def registry_name(self):
        """返回实体的friendly_name属性."""
        return self._friendly_name

    @property
    def state(self):
        """返回当前的状态."""
        return self._state

    @property
    def icon(self):
        """返回icon属性."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """返回unit_of_measuremeng属性."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """设置其它一些属性值."""
        if self._state is not None:
            return {
                ATTR_ATTRIBUTION: ATTRIBUTION,
                ATTR_UPDATE_TIME: self._updatetime
            }

    @asyncio.coroutine
    def async_update(self):
        """update函数变成了async_update."""
        self._updatetime = self._data.updatetime

        if self._type == "3hour":
            self._state = self._data.hour_3[0]+' '+self._data.hour_3[1]+' '+self._data.hour_3[2]
            
            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_3[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "6hour":
            self._state = self._data.hour_6[0]+' '+self._data.hour_6[1]+' '+self._data.hour_6[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_6[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "9hour":
            self._state = self._data.hour_9[0]+' '+self._data.hour_9[1]+' '+self._data.hour_9[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_9[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "12hour":
            self._state = self._data.hour_12[0]+' '+self._data.hour_12[1]+' '+self._data.hour_12[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_12[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "15hour":
            self._state = self._data.hour_15[0]+' '+self._data.hour_15[1]+' '+self._data.hour_15[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_15[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "18hour":
            self._state = self._data.hour_18[0]+' '+self._data.hour_18[1]+' '+self._data.hour_18[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_18[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "21hour":
            self._state = self._data.hour_21[0]+' '+self._data.hour_21[1]+' '+self._data.hour_21[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_21[1] in j:
                    self._icon = 'mdi:weather-'+i

        elif self._type == "24hour":
            self._state = self._data.hour_24[0]+' '+self._data.hour_24[1]+' '+self._data.hour_24[2]

            for i, j in CONDITION_CLASSES.items():
                if self._data.hour_24[1] in j:
                    self._icon = 'mdi:weather-'+i


class WeatherData(object):
    """天气相关的数据，存储在这个类中."""

    def __init__(self, hass, city, appkey):
        """初始化函数."""
        self._hass = hass

        self._url = "https://way.jd.com/he/freeweather"
        self._params = {"city": city,
                        "appkey": appkey}
        self._hour_3 = None
        self._hour_6 = None
        self._hour_9 = None
        self._hour_12 = None
        self._hour_15 = None
        self._hour_18 = None
        self._hour_21 = None
        self._hour_24 = None
        self._updatetime = None

    @property
    def hour_3(self):
        """温度."""
        return self._hour_3

    @property
    def hour_6(self):
        """湿度."""
        return self._hour_6

    @property
    def hour_9(self):
        """pm2.5."""
        return self._hour_9

    @property
    def hour_12(self):
        """hour_12."""
        return self._hour_12
    
    @property
    def hour_15(self):
        """hour_15."""
        return self._hour_15
    
    @property
    def hour_18(self):
        """hour_18."""
        return self._hour_18

    @property
    def hour_21(self):
        """hour_21."""
        return self._hour_21

    @property
    def hour_24(self):
        """hour_21."""
        return self._hour_24

    @property
    def updatetime(self):
        """更新时间."""
        return self._updatetime

    @asyncio.coroutine
    def async_update(self, now):
        """从远程更新信息."""
        _LOGGER.info("Update from JingdongWangxiang's OpenAPI...")

        """
        # 异步模式的测试代码
        import time
        _LOGGER.info("before time.sleep")
        time.sleep(40)
        _LOGGER.info("after time.sleep and before asyncio.sleep")
        asyncio.sleep(40)
        _LOGGER.info("after asyncio.sleep and before yield from asyncio.sleep")
        yield from asyncio.sleep(40)
        _LOGGER.info("after yield from asyncio.sleep")
        """

        # 通过HTTP访问，获取需要的信息
        # 此处使用了基于aiohttp库的async_get_clientsession
        try:
            session = async_get_clientsession(self._hass)
            with async_timeout.timeout(15, loop=self._hass.loop):
                response = yield from session.post(
                    self._url, data=self._params)

        except(asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Error while accessing: %s", self._url)
            return

        if response.status != 200:
            _LOGGER.error("Error while accessing: %s, status=%d",
                          self._url,
                          response.status)
            return

        result = yield from response.json()

        if result is None:
            _LOGGER.error("Request api Error")
            return
        elif result["code"] != "10000":
            _LOGGER.error("Error API return, code=%s, msg=%s",
                          result["code"],
                          result["msg"])
            return

        # 根据http返回的结果，更新数据
        hourlymsg = result["result"]["HeWeather5"][0]["hourly_forecast"]
        self._hour_3 = [hourlymsg[0]["date"][-5:], hourlymsg[0]["cond"]["txt"], hourlymsg[0]["tmp"]]
        self._hour_6 = [hourlymsg[1]["date"][-5:], hourlymsg[1]["cond"]["txt"], hourlymsg[1]["tmp"]]
        self._hour_9 = [hourlymsg[2]["date"][-5:], hourlymsg[2]["cond"]["txt"], hourlymsg[2]["tmp"]]
        self._hour_12 = [hourlymsg[3]["date"][-5:], hourlymsg[3]["cond"]["txt"], hourlymsg[3]["tmp"]]
        self._hour_15 = [hourlymsg[4]["date"][-5:], hourlymsg[4]["cond"]["txt"], hourlymsg[4]["tmp"]]
        self._hour_18 = [hourlymsg[5]["date"][-5:], hourlymsg[5]["cond"]["txt"], hourlymsg[5]["tmp"]]
        self._hour_21 = [hourlymsg[6]["date"][-5:], hourlymsg[6]["cond"]["txt"], hourlymsg[6]["tmp"]]
        self._hour_24 = [hourlymsg[7]["date"][-5:], hourlymsg[7]["cond"]["txt"], hourlymsg[7]["tmp"]]
        self._updatetime = result["result"]["HeWeather5"][0]["basic"]["update"]["loc"]
