import sys
import io
from urllib.request import urlretrieve
from os import environ, getcwd, path, mkdir
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from google.cloud import vision

import util.format

NAME = "Non-text Content"
DESCRIPTION = """All non-text content that is presented to the user has a text alternative
                  that serves the equivalent purpose, except for certain situations"""
LINK = "https://www.w3.org/TR/WCAG21/#non-text-content"
VERSION = 1
SCRIPT_DIR = path.dirname(path.realpath(__file__))

# Set env for google API credentials
environ["GOOGLE_APPLICATION_CREDENTIALS"] = path.join(getcwd(), "credentials", "google_api.json")

def run(driver):
  print(f"Printing title from {NAME}: {driver.title}")

  client = vision.ImageAnnotatorClient() # Google Cloud Vision Client

  try:
    mkdir(path.join(SCRIPT_DIR, "_result"), mode=0o777)
  except FileExistsError:
    pass
  except Exception as err:
    print(f"[Error] {NAME} rule failed execution:", err, "\n")
    return

  images = driver.find_elements(By.TAG_NAME, "img")

  if len(images):
    result = {
      
      "fail": [],
      "success": [],
      "visible": 0,
    }
    for i, image in enumerate(images):
      if image.is_displayed() and image.is_enabled():
        result['visible'] += 1
  
      properties = {
        "class": f".{image.get_attribute('class')}" if (image.get_attribute('class') != '') else '',
        "id": f"#{image.get_attribute('id')}" if (image.get_attribute('id') != '') else '',
        "alt": image.get_attribute('alt'),
        "src": image.get_attribute('src'),
      }
      properties["css_selector"] = f"img{properties['id']}{properties['class']}"
      status = True if (properties['alt'] != '') else False

      if status:
        #print(f"[Success] ({i}) '{properties['css_selector']}' has an alternative text: '{properties['alt']}'")
        result['success'].append(properties)
      else:
        #print(f"[Fail] ({i}) '{properties['css_selector']}' does not have an alternative text!")
        result['fail'].append(properties)
  
    success_count = len(result['success'])
    fail_count = len(result['fail'])
    visible_count = result['visible']
    images_count = len(images)
    #print("\n------ Result -----")
    #print(f"Total images: {images_count} where only {visible_count} are visible")
    #print(f"Images with an alternative text: {success_count}")
    #print(f"Images without an alternative text: {fail_count}")
    print(f"Images with alt-text: {int((success_count/images_count) * 100)}% ({success_count}/{images_count})")


    translations={
      "logo":["logo","icon"]
    }

    ## testing
    try:
      correct = 0
      incorrect = 0
      for i, image in enumerate(result['success']):
        correctAlt = False
        percentage = (i / success_count) * 100

        #print(f"[{percentage:.1f}%] Downloading image", end='\r')
        file_name, headers = urlretrieve(image['src'], path.join(SCRIPT_DIR, "_result", image['alt'] + '.jpg'))

        #print(f"[{percentage:.1f}%] Opening image", end='\r')
        with io.open(file_name, 'rb') as f:
          content = f.read()
        
        vision_image = vision.Image(content=content)
        #print(f"[{percentage:.1f}%] Identifying images for alt text corectness", end='\r')
        response = client.label_detection(image=vision_image)
        labels = response.label_annotations

        #print("                                                                          ")
        #print(f"Labels for '{image['alt']}':")
        
        

        for label in labels:
          labelText = label.description.lower()

          checks = [labelText]
          if labelText in translations:
            checks = translations[labelText]
          
          for check in checks:

            if check in image['alt'].lower() or image['alt'].lower() in check:
            
              correctAlt = True
        

        if correctAlt:
          correct+=1
        else:
          incorrect+=1
        if i==1:
          break
      print(f"{correct/incorrect*100}% of alt text matches image")
    except Exception as err:
      print(f"[Error] {NAME} rule failed execution:", err, '\n')




  # do the required tests for this rule
  # return something? maybe number of errors, some percentage, yada yada
  pass