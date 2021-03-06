import sys, re, eel
from os import environ, getcwd, path, mkdir
from shutil import rmtree
from urllib.request import urlretrieve

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from google.cloud import vision

# Custom imports
import util.errors as CS27Exceptions
from util.print import *
import util.format as CS27Format
import util.gui as CS27Gui

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ID = SCRIPT_DIR.split('\\')[-1]
NAME = "Non-text Content"
DESCRIPTION = """All non-text content that is presented to the user has a text alternative
                  that serves the equivalent purpose, except for certain situations"""
LINK = "https://www.w3.org/TR/WCAG21/#non-text-content"
VERSION = 1

# Set env for google API credentials
environ["GOOGLE_APPLICATION_CREDENTIALS"] = path.join(getcwd(), "credentials", "google_api.json")

def run(driver):
  tmp_folder = path.join(SCRIPT_DIR, "_tmp")
  if (not path.exists(tmp_folder)):
    mkdir(tmp_folder, mode=0o777)

  results_percentage = None

  images = driver.find_elements(By.TAG_NAME, "img")
  if (len(images)):
    alt_result = {
      "fail": [],
      "success": [],
      "visible": 0,
    }

    for image in images:
      if image.is_displayed() and image.is_enabled():
        alt_result['visible'] += 1
  
      properties = {
        "css": CS27Format.css_selector(driver, image),
        "alt": image.get_attribute('alt'),
        "src": image.get_attribute('src'),
      }
      status = True if (properties['alt'] != '') else False
      if (status):
        alt_result['success'].append(properties)
      else:
        print_error(f"'{properties['css']}' does not have an alternative text!")
        alt_result['fail'].append(properties)
        CS27Gui.run_eel('send_rule_result_event')(ID, 'fail', f"'{properties['css']}' does not have an alternative text!")
  
    # Detect image content, check if matches with label
    # Load custom translations
    with open(path.join(SCRIPT_DIR, "translations.txt")) as translation_file:
      translations = {}
      for line in translation_file:
        parsed_line = line.split(":")
        keyword = parsed_line[0]
        values = parsed_line[1].split(",")
        translations[keyword] = values
    
    # Initialize content result
    content_result = {
      "fail": [],
      "success": [],
    }

    client = vision.ImageAnnotatorClient() # Google Cloud Vision Client

    # Loop through images that have an "alt" attribute
    for image in alt_result['success']:
      # Download the image and read its bytes
      image_file_name, headers = urlretrieve(image['src'], path.join(tmp_folder, f"{image['alt']}.jpg"))
      with open(image_file_name, 'rb') as image_file:
        content = image_file.read()
      
      vision_image = vision.Image(content=content)
      response = client.label_detection(image=vision_image)
      labels = response.label_annotations

      regex_labels = []
      for label in labels:
        label_text = label.description.lower()
        # Append all the translations found for a label into the regex label matcher list
        if (label_text in translations):
          regex_labels.append('|'.join(translations[label_text]))
        # Append the label itself into the regex label matcher list
        regex_labels.append(label_text)

      # Compile the regex and test it against the alt image
      regex_check = re.compile(f"({'|'.join(regex_labels)})", re.IGNORECASE)
      regex_result = regex_check.findall(image['alt'])
      if (len(regex_result)):
        content_result['success'].append(image)
        CS27Gui.run_eel('send_rule_result_event')(ID, 'success', f"'{image['css']}' alternative text: \"{image['alt']}\" matches the image content!")
      else:
        print_error(f"'{image['css']}' alternative text: \"{image['alt']}\" does not match the image content!")
        content_result['fail'].append(image)
        CS27Gui.run_eel('send_rule_result_event')(ID, 'fail', f"'{image['css']}' alternative text: \"{image['alt']}\" does not match the image content!")
    
    success_count = len(content_result['success'])
    fail_count = len(content_result['fail']) + len(alt_result['fail'])
    images_count = success_count + fail_count

    results_percentage = (success_count/images_count)
      
    if (path.exists(tmp_folder)):
      rmtree(tmp_folder)

    if (results_percentage != None):
      return results_percentage * 100, "% of the headers match their immediate content"
  else:
    return None, "Page has no images"

