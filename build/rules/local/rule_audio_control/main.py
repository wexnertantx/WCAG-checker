import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import imagehash
from PIL import Image
import os


NAME = "Audio Control"
DESCRIPTION = """If any audio on a Web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level."""
LINK = "https://www.w3.org/TR/WCAG21/#headings-and-labels"
VERSION = 1


def format_css_selector(driver, element):
    elem_tag = driver.execute_script("return arguments[0].tagName.toLowerCase();", element)
    elem_class = f".{element.get_attribute('class')}" if (element.get_attribute('class') != '') else ''
    elem_id = f"#{element.get_attribute('id')}" if (element.get_attribute('id') != '') else ''
    return f"{elem_tag}{elem_id}{elem_class}"


def run(driver):
    print(f"Printing title from {NAME}: {driver.title}")
    WebDriverWait(driver, 10)
    time.sleep(2)

    videos = driver.find_elements(By.TAG_NAME, "video")
    audios = driver.find_elements(By.TAG_NAME, "audio")

    print(videos)
    print(audios)
    VACounter = 0
    VCCounter = 0
    AACounter = 0
    ACCounter = 0
    
    
    #Check videos for attributes
    print("\n####--Video Section--####")
    if len(videos):
        print("\n---Video Autoplay---")
        for video in videos:
            properties = {
                "class": f".{video.get_attribute('class')}" if (video.get_attribute('class') != '') else '',
                "id": f"#{video.get_attribute('id')}" if (video.get_attribute('id') != '') else '',
                "autoplay": video.get_attribute('autoplay'),
            }
            css_selector = f"media{properties['id']}{properties['class']}"

            if properties["autoplay"] is None:
                print(f"<Video Element>: --{css_selector}-- has autoplay disabled")
            else:
                first = "vid1.png"
                second = "vid2.png"
                location = video.location
                size = video.size
                driver.save_screenshot(first)
                x = location['x']
                y = location['y']
                width = location['x']+size['width']
                height = location['y']+size['height']
                im = Image.open(first)
                im = im.crop((int(x), int(y), int(width), int(height)))
                vidstarthash = imagehash.average_hash(im)
                print("Start hash: ", vidstarthash)
                time.sleep(4)
                driver.save_screenshot(second)
                im = Image.open(second)
                im = im.crop((int(x), int(y), int(width), int(height)))
                videndhash = imagehash.average_hash(im)
                print("Start hash: ", videndhash)

                if (vidstarthash != videndhash):
                    VACounter += 1
                    print(f"<Video Element> == {css_selector}-- has autoplay enabled")
                else:
                    print(f"<Video Element> -- {css_selector}-- does not have autoplay enabled")

                remove_files(first, second)
        print("Total video elements with autoplay: " + str(VACounter))
        print("Total video elements without autoplay: " + str(len(videos) - VACounter))
                
                
        #Check for Video Contols
        print("\n---Video Control---")
        for video in videos:
            properties = {
                "class": f".{video.get_attribute('class')}" if (video.get_attribute('class') != '') else '',
                "id": f"#{video.get_attribute('id')}" if (video.get_attribute('id') != '') else '',
                "controls": video.get_attribute('controls'),
            }
            css_selector = f"video{properties['id']}{properties['class']}"
            
            if properties["controls"] != None:
                VCCounter += 1
                print(f"<Video Element>: --{css_selector}-- has control attribute")
            else:
                print(f"<Video Element>: --{css_selector}-- has no control attribute")
        print("Total video elements with controls: " + str(VCCounter))
        print("Total video elements without controls: " + str(len(videos) - VCCounter))
  

    else:
        print("No video elements found on page")
    
    
    #check audios for attributes
    print("\n####--Audio Section--####")
    if len(audios):
    
        #Check for audio autoplay
        print("\n---Audio Autoplay---")
        for audio in audios:
            properties = {
                "class": f".{audio.get_attribute('class')}" if (audio.get_attribute('class') != '') else '',
                "id": f"#{audio.get_attribute('id')}" if (audio.get_attribute('id') != '') else '',
                "autoplay": audio.get_attribute('autoplay'),
            }
            css_selector = f"audio{properties['id']}{properties['class']}"
            
            if properties["autoplay"] is None:
                print(f"<Audio Element>: --{css_selector}-- has autoplay disabled")
            else:
                AACounter += 1
                print(f"<Audio Element>: --{css_selector}-- has autoplay enabled")
                
        print("\n---Audio Control---")
        
        for audio in audios:
            properties = {
                "class": f".{audio.get_attribute('class')}" if (audio.get_attribute('class') != '') else '',
                "id": f"#{audio.get_attribute('id')}" if (audio.get_attribute('id') != '') else '',
                "controls": audio.get_attribute('controls'),
            }
            css_selector = f"audio{properties['id']}{properties['class']}"
            
            if properties["controls"] != None:
                ACCounter += 1
                print(f"<Audio Element>: --{css_selector}-- has control attribute")
            else:
                print(f"<Audio Element>: --{css_selector}-- has no control attribute")
        print("Total audio elements with controls: " + str(ACCounter))
        print("Total audio elements without controls: " + str(len(audios) - ACCounter))
    else:
        print("No audio elements found on the page")
        

    #Summary output
    print("\n####--Summary of Rule--####")
    print("Total rule failures: " + str(VACounter + VCCounter + AACounter + ACCounter))
    print("See above for details.")


    


def remove_files(firstimg, secimg):
    if os.path.exists(firstimg):
        os.remove(firstimg)
    if os.path.exists(secimg):
        os.remove(secimg)
    print("Removed created files....")
