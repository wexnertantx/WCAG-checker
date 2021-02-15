import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import spacy
from spacy_langdetect import LanguageDetector
from spacy.pipeline import Sentencizer
from spacy.lang.xx import MultiLanguage
from subprocess import check_output


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
    cmd='python -m spacy download xx_ent_wiki_sm'
    check_output(cmd,shell=True).decode()
    #load multi language (xx) and create pipelines, sentencizer for sentence boundaries
    nlp = spacy.load("xx_ent_wiki_sm")
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    nlp.add_pipe(LanguageDetector(),name='language_detector', last=True)
    
    print(f"Printing title from {NAME}: {driver.title}")
    WebDriverWait(driver, 10)
    time.sleep(2)
    
    #get html code, extract language element for cross checking
    html_tag = driver.find_elements(By.TAG_NAME, "html")
    lang = html_tag[0].get_attribute("lang")
    #get <p> texts
    ptext=driver.find_elements_by_tag_name('p')
    total_sentence_count,matching_sentence_count=0,0
    #strip all white spaces and use NLP to recognise text and language off wordbank, compare with html lang tag with score comparison
    #A LITTLE BUGGY WITH BAD HTML CODES
    if len(lang):

        print("Detected <lang> tag: ",lang)

        for p in ptext:
            total_sentence_count=total_sentence_count+1
            p.text.strip()
            #print(p.text)
            txt=nlp(p.text)
            langscore=txt._.language
            lan=langscore.get('language')
            #print(langscore)
            if (lan is not lang) and (langscore.get('score')<0.7):
                print("Text \""+p.text+"\" is not of proper sentence or is of another language.")
                print(langscore)
            else:
                matching_sentence_count=matching_sentence_count+1
        print("%.2f%% of the page matches <lang> tag"%(((matching_sentence_count/total_sentence_count)*100)))
    else:
        print("Page has no <lang> attribute")