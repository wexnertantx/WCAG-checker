from os import path, mkdir
from shutil import rmtree
import time, eel

import imagehash
from PIL import Image

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Custom imports
import util.errors as CS27Exceptions
from util.print import *
import util.format as CS27Format
import util.gui as CS27Gui

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ID = SCRIPT_DIR.split('\\')[-1]
NAME = "Audio Control"
DESCRIPTION = """If any audio on a Web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level."""
LINK = "https://www.w3.org/TR/WCAG21/#headings-and-labels"
VERSION = 1

###
# Amount of parent levels to look through to find custom media controls, default 2
#   <div>
#     <div>
#        <video></video>
#     </div>
#    <div class="controls"></div>          <-- Custom video controls will be found here
#   </div>
###
CONTROLS_PARENT_LIMIT = 2

def run(driver):
  time.sleep(2)

  tmp_folder = path.join(SCRIPT_DIR, "_tmp")
  if (not path.exists(tmp_folder)):
    mkdir(tmp_folder, mode=0o777)

  results_percentage = None

  audio = driver.find_elements(By.TAG_NAME, "audio")
  video = driver.find_elements(By.TAG_NAME, "video")
  media = audio + video

  media_autoplay = []
  media_control = {
    'fail': [],
    'success': [],
  }

  if (len(media)):
    for element in media:
      properties = {
        "self": element,
        "tag": driver.execute_script("return arguments[0].tagName.toLowerCase();", element),
        "autoplay": element.get_attribute('autoplay'),
        "controls": element.get_attribute('controls'),
      }

      # If video does not have autoplay specified, hard check using video frames
      if (properties['autoplay'] == 'None' and properties['tag'] == 'video'):
        first = path.join(tmp_folder, "video-1.png")
        second = path.join(tmp_folder, "video-2.png")
        location = element.location
        size = element.size
        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']

        # Save two screenshots with a 4-second interval
        driver.save_screenshot(first)
        im = Image.open(first)
        im = im.crop((int(x), int(y), int(width), int(height)))
        start_hash = imagehash.average_hash(im)
        time.sleep(4)
        driver.save_screenshot(second)
        im = Image.open(second)
        im = im.crop((int(x), int(y), int(width), int(height)))
        end_hash = imagehash.average_hash(im)

        # If the screenshots differ, the video is automatically playing
        if (start_hash != end_hash):
          properties['autoplay'] = True

      if (properties['autoplay'] != None):
        media_autoplay.append(properties)
  else:
    return None, "Page has no media"

  if (len(media_autoplay)):
    for element in media_autoplay:
      parent = element['self']
      found = True if (element['controls'] != None) else False
      level = 0
      while (found == False and level < CONTROLS_PARENT_LIMIT):
        parent = driver.execute_script("return arguments[0].parentNode;", parent)
        controls = list(filter(
          lambda c: (driver.execute_script("return arguments[0].tagName.toLowerCase();", c) != element['tag']), # Exclude self
          parent.find_elements(By.XPATH, ".//*[contains(@role, 'button') or contains(translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'control')] | .//button")
        ))

        # Break out of the loop when controls have been found
        if (len(controls)):
          found = True
        else:
          level += 1

      element_css = CS27Format.css_selector(driver, element['self'])
      if (found):
        media_control['success'].append(element)
        CS27Gui.run_eel('send_rule_result_event')(ID, 'success', f"'{element_css}' has autoplay enabled and controls have been found!")
      else:
        media_control['fail'].append(element)
        print_error(f"'{element_css}' has autoplay enabled but no controls could be found!")
        CS27Gui.run_eel('send_rule_result_event')(ID, 'fail', f"'{element_css}' has autoplay enabled but no controls could be found!")

  if (path.exists(tmp_folder)):
    rmtree(tmp_folder)

  success_count = len(media_control['success'])
  fail_count = len(media_control['fail'])
  autoplay_count = success_count + fail_count

  results_percentage = (success_count/autoplay_count)

  if (results_percentage != None):
    return results_percentage * 100, "% of the media that have autoplay enabled have controls as well"
    
