# Actions/action_router.py

from Actions.greetings import Greetings
from Actions.date_time import DateTimeAction
from Actions.open_websites import OpenWebsites
from Actions.quit import Quit
from Actions.app_opener import AppOpener
from Actions.brightness_control import Brightness
from Actions.lock_screen import LockScreen
from Actions.system_status import SystemStatus
from Actions.wifi_status import WifiStatus
from Actions.volume_control import VolumeControl
from Actions.battery_status import BatteryStatus


class ActionRouter:

    def __init__(self):
        self.greetings = Greetings()
        self.date_time = DateTimeAction()
        self.open_websites = OpenWebsites()
        self.quit = Quit()
        self.app_opener = AppOpener()
        self.brightness_control = Brightness()
        self.lock_screen = LockScreen()
        self.ram_cpu_status = SystemStatus()
        self.wifi_status = WifiStatus()
        self.volume_control = VolumeControl()
        self.battery_status = BatteryStatus()


    def action_handler(self, text: str):
        response = None

        response, action = self.greetings.get_response(text)
        if response:
            return response, action

        response, action = self.date_time.get_response(text)
        if response:
            return response, action

        response, action = self.open_websites.get_response(text)
        if response:
            return response, action
        
        response, action = self.quit.get_response(text)
        if response:
            return response, action
        
        response, action = self.app_opener.get_response(text)
        if response:
            return response, action
        
        response, action = self.brightness_control.get_response(text)
        if response:
            return response, action
        
        response, action = self.lock_screen.get_response(text)
        if response:
            return response, action
        
        response, action = self.ram_cpu_status.get_response(text)
        if response:
            return response, action
        
        response, action = self.wifi_status.get_response(text)
        if response:
            return response, action
        
        response, action = self.volume_control.get_response(text)
        if response:
            return response, action
        
        response, action = self.battery_status.get_response(text)
        if response:
            return response, action
    
        
        return response, None