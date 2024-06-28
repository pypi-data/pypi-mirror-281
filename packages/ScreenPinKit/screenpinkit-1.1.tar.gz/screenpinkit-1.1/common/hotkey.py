# coding:utf-8
import time
from PyQt5.QtCore import *
from system_hotkey import *

class KeyboardEx(QObject):
    handleSignal = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.hk = SystemHotkey()
        self._pressedRecord = {}
        self.intervalTime = 400
        self.handleSignal.connect(self.handleKeyCallback)
        self.map_callbacks = {}

    def handleKeyCallback(self, key):
        if key in self.map_callbacks:
            self.map_callbacks[key]()

    def reset(self):
        self.hk.unregister()

    def __convertToHotkey(self, key:str) -> list:
        result = []
        for str in key.split("+"):
            temp = str.replace("ctrl", "control")
            temp = temp.lower()
            if len(temp) > 0:
                result.append(temp)
        return result

    def addHotKey(self, key:str, callback, overwrite=False):
        hotkey = self.__convertToHotkey(key)
        if len(hotkey) == 0:
            return
        self.map_callbacks[key] = callback
        self.hk.register(hotkey, callback=lambda _: self.handleSignal.emit(key), overwrite=overwrite)

    def addHotKeyEx(self, key:str, times, callback):
        hotkey = self.__convertToHotkey(key)
        if len(hotkey) == 0:
            return
        self.hk.register(hotkey, callback=lambda _: self.updatePressTime(key))

        defaultValue = {
            "lastPressTime" : 0,
            "triggerTimes" : 0,
            "matchTimes" : times,
        }
        self._pressedRecord[key] = defaultValue
        real_key = f"{key}_{defaultValue['matchTimes']}"
        self.map_callbacks[real_key] = callback

    def updatePressTime(self, key):
        matchValue = self._pressedRecord[key]
        currentPressedTime = int(round(time.time() * 1000))
        differentTime = currentPressedTime - matchValue["lastPressTime"]
        matchValue["lastPressTime"] = currentPressedTime
        matchValue["triggerTimes"] = matchValue["triggerTimes"] + 1

        # 超过特定间隔时间重算
        if differentTime > self.intervalTime:
            matchValue["triggerTimes"] = 1

        # 满足检测次数则响应
        if matchValue["triggerTimes"] >= matchValue["matchTimes"]:
            matchValue["triggerTimes"] = 0
            real_key = f"{key}_{matchValue['matchTimes']}"
            self.handleSignal.emit(real_key)