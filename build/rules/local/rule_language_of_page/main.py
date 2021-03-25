from os import path
import time, re, json

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import detectlanguage
detectlanguage.configuration.api_key = "3af1a02a97678b5ab470959a24481d25"
# TODO: Change the API Key
# Enable secure mode (SSL) if you are passing sensitive data
# detectlanguage.configuration.secure = True

# Custom imports
import util.errors as CS27Exceptions
from util.print import *

NAME = "Language of Page"
DESCRIPTION = """The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text."""
LINK = "https://www.w3.org/WAI/WCAG21/Understanding/language-of-page.html"
VERSION = 1
SCRIPT_DIR = path.dirname(path.realpath(__file__))
SKIP = False

def run(driver):
  if (SKIP):
    raise CS27Exceptions.NoResult("This rule is flagged to be skipped, check the SKIP flag in your rule!")
  
  try:
    results_percentage = None
    
    html = driver.find_elements(By.TAG_NAME, "html")
    properties = {
      'lang': html[0].get_attribute("lang")
    }

    page_text = html[0].text.split('\n')
    lang_results = {
      'fail': [],
      'success': [],
      'avg_confidence': 0,
    }

    if len(properties['lang']):
      avg_confidence = lang_results['avg_confidence']
      for text in page_text:
        if (len(text) == 0):
          continue

        lang_score = detectlanguage.detect(text)
        if (len(lang_score) == 0):
          continue

        lang = lang_score[0]['language']
        reliable = lang_score[0]['isReliable']
        confidence = lang_score[0]['confidence']
        if (lang == properties['lang'] and reliable == True and confidence > 2.5):
          lang_results['success'].append(text)
        else:
          lang_results['fail'].append(text)
          if (lang == properties['lang'] and confidence <= 2.5):
            print_error(f"'{text}' matches the page language ({lang}) but has a low confidence score of {confidence}")
          elif (lang == properties['lang'] and reliable == True):
            print_error(f"'{text}' matches the page language ({lang}) but the result is unreliable")
          else:
            print_error(f"'{text}' with language ({lang}) failed to match the page language ({properties['lang']})")

      success_count = len(lang_results['success'])
      fail_count = len(lang_results['fail'])
      text_count = len(page_text)

      results_percentage = (success_count/text_count)

      if (results_percentage != None):
        return results_percentage * 100, f"% of the page matches the lang attribute \"{properties['lang']}\""
    else:
      return None, "Page has no lang attribute within the <html> tag"
    
  except Exception as err:
    print_error(f"[Error] {NAME} rule failed execution:", err, '\n')
