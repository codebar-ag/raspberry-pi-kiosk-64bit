
from config.gtconf import CONFIG 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

#NOTE: #*  There could be a decoupling of BROWSER and KIOSK for better Code decoupling. (Ill maybe change this later)

default_on_start_url = CONFIG.screenurls.browser_start_url # type: ignore
default_on_start_url_is_internal = CONFIG.screenurls.browser_start_url_is_internal # type: ignore

class Browser(): 
    """QUICK Browser CLASS

    Controlls the Selenium browser kiosk
    to handle selenium Browser and urls

    takes: 
    on_start_url -> (str) THE URL THE BROWSER STARTS. BEVOR AUTH WITH SERVER. (GOOD PLACE FOR NOTHER SPLASH SCREEN)
    on_start_url_internal -> (bool) Set to True if int. rel. path. to make fileurl 
    on_start_url, taken from config file bye default.
    """

    def __init__(self, on_start_url=default_on_start_url, on_start_url_internal=default_on_start_url_is_internal):      
        self.on_start_url = self._internal_path_to_url(on_start_url) if on_start_url_internal else on_start_url
        self.last_url = None
        self.current_url = None
        self.state_open = False
        self.url_history = [] # unused save url history.

    
    def update_window_url(self, url, is_internal=False):
        """update the browser url resived from backend.
        
        is_internal: (Bool) If page is relativ internal set True and will parse to Absolute Internal File URL
        
        selenium will raise: selenium.common.exceptions.InvalidArgumentException (Maybe Automaticly catch)
        
        Will not change if current_url is (new) url (to prevent unneded reloading)
        """
        # the driver class has current url function returning the real browser url. interesting for redirects or querys

        if is_internal:
            url = self._internal_path_to_url(url)

        if self.current_url == url: 
            msg = f"SAME URLS: \nBrowser is already on {url}"
            print(msg)            
            #log
            return True

        else: #* Different URL

            self.driver.get(url)
            self.last_url = self.current_url
            self.current_url = url
            
            msg = f"CHANGED URLS: \nLAST_URL {self.last_url} \nNEW_URL {self.current_url}"
            print(msg)
            #log
            return True


    def _start_kiosk(self):
        """ Start the Kiosk 
        (Start Chrome Driver in kiosk mode)
        assigns self.driver with the chrome driver

        start chrome browser with start url.
        """

        chrome_options = Options()
        chrome_options.add_argument("--kiosk")
        #chrome_options.add_argument("--kiosk --noerrdialogs --disable-infobars")

        #removes automation notice on window
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(self.on_start_url)
        self.state_open = True


    @staticmethod
    def _internal_path_to_url(internal_path):
        """ Relative Internal Fallbacks Path to Browser File URL

        Config File hold internal relative Paths        
        Turn relative internal path pointing to index pages to openable absolute urls.
        return: (string) Absolute Internal File URL
        """
        relative_fallback_path = Path(internal_path)
        absolute_file_url = "file://" + str(Path.cwd().joinpath(relative_fallback_path))
        return absolute_file_url


if __name__ == '__main__':

    # CLASS TESTS 
    testuri = 'https://www.python.org/dev/peps/pep-0020/#id2'
    browser = Browser(on_start_url=testuri)
    browser._start_kiosk()

    x = 1