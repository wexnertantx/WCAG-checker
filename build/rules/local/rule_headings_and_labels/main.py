from bs4 import BeautifulSoup
import time,re
import spacy
from subprocess import check_output
#pip install -U spacy
#python -m spacy download en_core_web_lg <-how do i install thiz in requirement.txt
#pip install beautifulsoup4


NAME = "Headings and Labels"
DESCRIPTION = """Headings and labels describe topic or purpose."""
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




    
def run(driver):
  cmd='python -m spacy download en_core_web_sm'
  check_output(cmd,shell=True).decode()
  nlp = spacy.load("en_core_web_lg")
  print(f"Printing title from {NAME}: {driver.title}")
  html=driver.page_source
  time.sleep(2)
  soup=BeautifulSoup(html,"lxml")
  headercounter=0
  overall_sim=0
  average_sim=0
  headertypes=re.compile('^h[1-6]$')


  for header in soup.find_all(headertypes):
    para=header.find_next_sibling(['p',headertypes])
    #if next_sibling.name==re.compile('^h[1-6]$'):
    #  continue
    if (para!=None):
      
      headercounter+=1
      headstripped=header.text
      head=nlp(headstripped)
      content=nlp(para.text)
      sim=head.similarity(content)
      
      overall_sim+=sim
      print(f"{bcolors.HEADER}Header text:{bcolors.ENDC}"+headstripped.strip())
      #print(f"{bcolors.OKBLUE}Paragraph text:{bcolors.ENDC}"+para.text)
      #print(f"{bcolors.WARNING} Similarity rate: {bcolors.ENDC} "+str(sim))
      if (sim<0.65):
            print(f"{bcolors.FAIL}Header needs to be more descriptive in comparison to content:\""+header.text+"\"")
  average_sim=100*(overall_sim/headercounter)
  if (average_sim>0.65):
    print(f"{bcolors.OKGREEN}Overall description relevancy rate: (PASS) {bcolors.ENDC} "+str(average_sim)+"%")
  else:
    print(f"{bcolors.FAIL}Overall description relevancy rate: (FAIL) {bcolors.ENDC} "+str(average_sim)+"%")
  pass