from os import path
import time, re

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Spacy imports
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from spacy.pipeline import Sentencizer
from spacy.lang.xx import MultiLanguage
from subprocess import check_output

# Custom imports
import util.errors as CS27Exceptions
from util.print import *

NAME = "Language of Page"
DESCRIPTION = """The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text."""
LINK = "https://www.w3.org/WAI/WCAG21/Understanding/language-of-page.html"
VERSION = 1
SCRIPT_DIR = path.dirname(path.realpath(__file__))
SKIP = False

@Language.factory("language_detector")
def create_language_detector(nlp, name):
  return LanguageDetector(language_detection_function=None)

def run(driver):
  if (SKIP):
    raise CS27Exceptions.NoResult("This rule is flagged to be skipped, check the SKIP flag in your rule!")
  
  try:
    output = check_output('spacy download xx_ent_wiki_sm', shell=True).decode()
    print_end_color()

    results_percentage = None

    # Load multi language (xx) and create pipelines, sentencizer for sentence boundaries
    nlp = spacy.load('xx_ent_wiki_sm')
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('language_detector', last=True)
    
    html = driver.find_elements(By.TAG_NAME, "html")
    properties = {
      'lang': html[0].get_attribute("lang")
    }

    page_text = html[0].text.split('\n')
    lang_results = {
      'fail': [],
      'success': [],
    }

    if len(properties['lang']):
      for text in page_text:
        if (len(text) == 0):
          continue

        nlp_text = nlp(text)
        lang_data = nlp_text._.language
        lang = lang_data.get('language')
        score = lang_data.get('score')
        if lang != properties['lang']:
          lang_results['fail'].append(text)
          print_error(f"'{text}' with language ({lang}) failed to match the page language ({properties['lang']})")
        else:
          lang_results['success'].append(text)

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
