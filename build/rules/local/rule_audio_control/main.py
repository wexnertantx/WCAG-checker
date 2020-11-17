from bs4 import BeautifulSoup
import time,re
import spacy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import PyV8

#pip install -U spacy
#python -m spacy download en_core_web_lg <-how do i install thiz in requirement.txt
#pip install beautifulsoup4


NAME = "Audio Control"
DESCRIPTION = """If any audio on a Web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level."""
LINK = "https://www.w3.org/TR/WCAG21/#headings-and-labels"
VERSION = 1
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


script="var list= document.getElementsByTagName('video').autoplay;return list;"

    
def run(driver):
  #nlp = spacy.load("en_core_web_lg")
  print(f"Printing title from {NAME}: {driver.title}")
  wait = WebDriverWait(driver, 10)
  wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'video')))
  #html=driver.page_source
  time.sleep(2)
  #soup=BeautifulSoup(html,"lxml")
  listvidautoplay=driver.execute_script(script)
  print(listvidautoplay)



