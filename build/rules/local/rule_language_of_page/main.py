import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

NAME = "Language of Page"
DESCRIPTION = """The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text."""
LINK = "https://www.w3.org/WAI/WCAG21/Understanding/language-of-page.html"
VERSION = 1

'''
def format_css_selector(driver, element):
    elem_tag = driver.execute_script("return arguments[0].tagName.toLowerCase();", element)
    elem_class = f".{element.get_attribute('class')}" if (element.get_attribute('class') != '') else ''
    elem_id = f"#{element.get_attribute('id')}" if (element.get_attribute('id') != '') else ''
    return f"{elem_tag}{elem_id}{elem_class}"
'''
    
def run(driver):
    print(f"Printing title from {NAME}: {driver.title}")
    WebDriverWait(driver, 10)
    time.sleep(2)
    
    #this part can probably be optimised later
    string = driver.page_source
    substring = "lang="
    for line in string.split():
        if substring in line:
            subLine = line.split('"')
            language = subLine[1]
    
    
    
    if len(language):
        #insert ai code to detect language
        
        #outputted string of language
        detectedLang = ""
        
        #I'll add more system output later if need be to show more helpful language
        if detectedLang == language:
            print("Match: Language of page matches html lang tag")
        else:
            print("Error: Language of page does not match html lang tag")
    else:
        print("Page has no lang attribute.")
