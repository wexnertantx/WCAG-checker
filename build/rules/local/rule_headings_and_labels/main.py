from os import path
import time, re, eel
import spacy
from subprocess import check_output

# Selenium imports
from selenium.webdriver.common.by import By

# Custom imports
import util.errors as CS27Exceptions
from util.print import *
import util.format as CS27Format
import util.gui as CS27Gui

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ID = SCRIPT_DIR.split('\\')[-1]
NAME = "Headings and Labels"
DESCRIPTION = """Headings and labels describe topic or purpose."""
LINK = "https://www.w3.org/TR/WCAG21/#headings-and-labels"
VERSION = 1

###
# Amount of text elements to look through in the next sibling to see if the content matches the header, default 2
#   <h1>Header</h1>
#   <div flex>
#     <div>Random text</div>
#     <div>Some text that matches the header content</div>
#     --- Script stops checking here, if it doesn't match until here mark header as failed ---
#     <div>Random text</div>
#     <div>Random text</div>
#   </div>
###
TEXT_ELEMENTS_LIMIT = 2

def getNextSibling(driver, element):
  return driver.execute_script("return arguments[0].nextElementSibling", element)

def run(driver):
  output = check_output('spacy download en_core_web_lg', shell=True).decode()
  print_end_color()

  results_percentage = None

  nlp = spacy.load("en_core_web_lg")
  header_elements = driver.find_elements(By.XPATH, '//h1|//h2|//h3|//h4|//h5|//h6')
  header_content = {
    'fail': [],
    'success': [],
  }

  if (len(header_elements)):
    for header in header_elements:
      if (len(header.text) == 0):
        header_content['fail'].append(header)
        print_error(f"Header {CS27Format.css_selector(driver, header)} does not have any text")
        continue
        
      sibling = getNextSibling(driver, header)
      header_tag = CS27Format.getElementTag(driver, header)
      while (sibling != None and CS27Format.getElementTag(driver, sibling) == header_tag):
        sibling = getNextSibling(driver, sibling)
      
      if (sibling == None):
        continue

      sibling_text_lines = sibling.text.split('\n')
      element_css = CS27Format.css_selector(driver, header)
      if (len(sibling_text_lines[0]) == 0):
        header_content['fail'].append(header)
        print_error(f'Header {element_css} does not have any content: "{header.text}"')
        CS27Gui.run_eel('send_rule_result_event')(ID, 'fail', f'Header {element_css} does not have any content: "{header.text}"')
        continue

      level = 0
      found = False
      while (found == False and level < TEXT_ELEMENTS_LIMIT and level < len(sibling_text_lines)):
        text = sibling_text_lines[level]
        nlp_header_text = nlp(header.text)
        nlp_content_text = nlp(text)
        score = nlp_header_text.similarity(nlp_content_text)

        if (score > 0.65):
          found = True
        else:
          level += 1

      if (found):
        header_content['success'].append(header)
        CS27Gui.run_eel('send_rule_result_event')(ID, 'success', f'Header {element_css} is descriptive enough to match the content: "{header.text}"')
      else:
        header_content['fail'].append(header)
        print_error(f'Header {element_css} not descriptive enough in comparison to content: "{header.text}"')
        CS27Gui.run_eel('send_rule_result_event')(ID, 'fail', f'Header {element_css} not descriptive enough in comparison to content: "{header.text}"')
    
    success_count = len(header_content['success'])
    fail_count = len(header_content['fail'])
    header_count = success_count + fail_count

    results_percentage = (success_count/header_count)

    if (results_percentage != None):
      return results_percentage * 100, "% of the headers match their immediate content"
  else:
    return None, "Page has no header tags"

  