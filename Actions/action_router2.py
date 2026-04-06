# Actions/action_router2.py

from Learning_ML.intent_predictor import IntentPredictor

from Actions.app_opener import AppOpener
from Actions.battery_status import BatteryStatus
from Actions.brightness_control import Brightness
from Actions.clipboard_reader import ClipboardReader
from Actions.date_time import DateTimeAction
from Actions.disk_status import DiskStatus
from Actions.doc_finder import DOCFinder
from Actions.folder_finder import FolderFinder
from Actions.greetings import Greetings
from Actions.groq_internet_access import Groq
from Actions.image_finder import ImageFinder
from Actions.internet_speed_test import InternetSpeed
from Actions.ip_address import IPAddress
from Actions.lock_screen import LockScreen
from Actions.media_control import MediaControl
from Actions.open_websites import OpenWebsites
from Actions.pdf_finder import PDFFinder
from Actions.ppt_finder import PPTFinder
from Actions.quit import Quit
from Actions.restart_pc import RestartPC
from Actions.screenshot import Screenshot
from Actions.shutdown_pc import ShutdownPC
from Actions.system_status import SystemStatus
from Actions.system_uptime import SystemUptime
from Actions.volume_control import VolumeControl
from Actions.wifi_status import WifiStatus


class ActionRouter():
    def __init__(self):
        self.predictor = IntentPredictor()
        self.internet_mode = False

        self.intent_map = {
            "open_app": AppOpener(),
            "battery_status": BatteryStatus(),
            "brightness_control": Brightness(),
            "clipboard_read": ClipboardReader(),   
            "date_time": DateTimeAction(),        
            "disk_status": DiskStatus(),
            "doc_search": DOCFinder(),
            "folder_search": FolderFinder(),
            "greeting": Greetings(),
            "image_search": ImageFinder(),
            "internet_speed": InternetSpeed(),
            "ip_address": IPAddress(),
            "lock_screen": LockScreen(),
            "media_control": MediaControl(),
            "open_website": OpenWebsites(),
            "pdf_search": PDFFinder(),
            "ppt_search": PPTFinder(),
            "quit": Quit(),
            "restart_pc": RestartPC(),
            "screenshot": Screenshot(),
            "shutdown_pc": ShutdownPC(),
            "system_status": SystemStatus(),
            "system_uptime": SystemUptime(),
            "volume_control": VolumeControl(),
            "wifi_status": WifiStatus()
        }

        # Groq class object outside the mapper because its working together with system actions
        # Now it will only work in Internet Mode
        self.groq = Groq()

    def action_handler(self, command : str):

        command = command.lower()

        # ===== MODE ACTIVATION =====

        INTERNET_MODE_ON_TRIGGER = ["access the internet" , "i need internet", "internet mode"]

        if any(word in command for word in INTERNET_MODE_ON_TRIGGER):
            self.internet_mode = True
            return "Internet mode activated.", "internet_on"
        
        INTERNET_MODE_OFF_TRIGGER = ["exit internet", "normal mode"]

        if any(word in command for word in INTERNET_MODE_OFF_TRIGGER):
            self.internet_mode = False
            return "Returning to normal mode.", "internet_off"


        # ===== INTERNET MODE =====
        if self.internet_mode:
            print("[MODE]: INTERNET MODE ON")

            return self.groq.get_response(command)


        # ===== NORMAL ML MODE =====
        intent, confidence = self.predictor.predict_intent(command)

        if confidence >= 0.5:
            action = self.intent_map.get(intent, None)

            if action:
                return action.get_response(command)


        # ===== FALLBACK =====
        for action in self.intent_map.values():
            response, action_func = action.get_response(command)
            if response:
                return response, action_func

        return "Sorry, I didn't understand that.", None