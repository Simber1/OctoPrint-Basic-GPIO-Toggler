# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import RPi.GPIO as GPIO

class BasicGPIOControlPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.ShutdownPlugin, 
    octoprint.plugin.ProgressPlugin, 
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.SettingsPlugin
):

    #Vars to store if a print is active or if a client is currently connected
    isClientConnected = False
    isPrinting = False

    #The pin to switch
    #TODO: Add settings for this
    pin = 4

    #Basic Helper functions to switch pins on and off
    def switchPinOn(self, pin):
        GPIO.output(pin,GPIO.HIGH)
        GPIO.output(pin,GPIO.LOW)
    def switchPinOff(self, pin):
        GPIO.output(pin,GPIO.LOW)
        GPIO.output(pin,GPIO.HIGH)

    #Do setup on startup. Maybe should be moved? Also needs to be rewrote to support reading from settings probably.
    def on_after_startup(self):
        # pin = self._settings.get(["pin"])
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin,GPIO.HIGH)

    #TODO: Change these to on plugin disable too
    #Turn off pin and cleanup on shutdown.
    def on_shutdown(self):
        GPIO.output(self.pin,GPIO.HIGH)
        GPIO.cleanup()

    #On Event, Checks for Print Starts and Stops as well as Client Connects and disconnects
    def on_event(self,event,payload):

        if event == "PrintStarted":
            self.isPrinting = True
            self.switchPinOn(self.pin)

        if event == "PrintDone":
            self.isPrinting = False
            if (self.isClientConnected == False):
                self.switchPinOff(self.pin)

        if event == "PrintFailed":
            self.isPrinting = False
            if (self.isClientConnected == False):
                self.switchPinOff(self.pin)

        if event == "ClientClosed":
            self.isClientConnected = False
            if (self.isPrinting == False):
                self.switchPinOff(self.pin)
            

        if event == "ClientOpened":
            self.isClientConnected = True
            self.switchPinOn(self.pin)

    # def get_settings_defaults(self):
    #     return dict(
    #         pin=4
    #     )
    
    # def on_settings_save(self, data):
    #     old_pin = self._settings.get_integer(["sub", "pin"])

    #     octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

    #     new_pin = self._settings.get_integer(["sub", "pin"])
    #     if old_pin != new_pin:
    #         self._logger.info("sub.some_flag changed from {old_pin} to {new_pin}".format(**locals()))


            

__plugin_name__ = "Basic GPIO Control"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A Basic \"GPIO Control\" plugin for OctoPrint"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = BasicGPIOControlPlugin()