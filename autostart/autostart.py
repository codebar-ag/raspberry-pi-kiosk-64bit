
import subprocess
import requests
import time
import json
import os

from config.gtconf import CONFIG 
from utils import rasputils

from interfaces.browser import Browser
from interfaces.device import Device

internal_fallback_url = CONFIG.screenurls.fallback # type: ignore
identification_url = CONFIG.screenurls.base + CONFIG.screenurls.identification # type: ignore

def identification_request(device):
    """ POST Request to auth & Register to Backend and receive information in return. 
    
    Body Sends:  MacAdress, Pi-Temperature.
    
    HEADERS need Accept and Content-Type set to application/json
    POSTMAN: https://documenter.getpostman.com/view/1711474/TzY3AaiV

    Expected Server Responses:
        200: OK will return json respone with url to display page.
        401: Unauthenticated - Wrong AUTH
        422: Invalid Request Body Parameters

    returns status_code, resposne_url

    """
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
    
    post_data = {
        'identification': device.mac_address(),
        'temperature': device.temperature(),
        }

    serverauth = (CONFIG.auth.user, CONFIG.auth.token) # type: ignore

    print(f'Homecall device temperatur: {device.temperature()}')
    print(f'Homecall device macadress: {device.mac_address()}')    
    # print(f"Homecall -> SERVERAUTH: {serverauth}")

    response = requests.post(identification_url, json=post_data, headers=headers, auth=serverauth)

    status_code = response.status_code
    
    try:
        resposne_url = response.json().get('url') # Target Display URL
    except json.decoder.JSONDecodeError: # response.json() raises error if no json response! # or only ask for json
        resposne_url = None
    
    except AttributeError:
        resposne_url = None

    print(f"Homecall answer: STATUS CODE: {status_code} URL: {resposne_url}")
    
    return status_code, resposne_url 


def event_loop(kiosk_browser, device):
    """MAIN EVENT LOOP Handler
    
    Makes identification_request after homecall_period (sek) provided in config
    to set kiosk browser url
    Handels browser based on status_code and server_response.
    Provides Disply(response)Url to the kiosk browser

    TODO: Refactor elif statements
    TODO: Implement different fallback screens for different events.
    TODO: Make deticated function for registering the device bevor entering mainloop!

    NOTE: ZeroDivisionError - At the beginning during development we should not catch all errors. rather catch them Debug them or Catch them explicitly.
    """

    while True:


        try:

            status_code, resposne_url = identification_request(device) # Homecall

            if status_code == 200: #* "OK" will return json respone with url to display page in resposne_url.
                
                assert resposne_url, 'No response(Display) url with SERVER 200!'
                
                kiosk_browser.update_window_url(resposne_url, is_internal=False)

            else: #?: Uncaught Server Response
                # FALLBACK SITE! add LOG MSG
                kiosk_browser.update_window_url(internal_fallback_url, is_internal=True)        # raise Exception('Uncaught Server Response')

        except ZeroDivisionError: 
            #? This will be called after an internal exception during the home call
            #! I will use a ZERODIVERROR here as place holder so we can see exceptions during development and catch them Explicit!
            #$ All these errors will lead to an internal Fallback page. currently this is not really usefull. because there is only 200 or fallback. 
            #$ and will only have loggig functionality for different logging messages
            kiosk_browser.update_window_url(internal_fallback_url, is_internal=True)


        time.sleep(CONFIG.homecall_period) # type: ignore


if __name__ == '__main__':

    kiosk_browser = Browser()
    
    device = Device()

    kiosk_browser._start_kiosk()

    event_loop(kiosk_browser, device)



