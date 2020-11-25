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

    medias = []
    for x in videos:
        medias.append(x)

    for y in audios:
        medias = medias.append(y)

    if len(medias):
        for media in medias:
            properties = {
                "class": f".{media.get_attribute('class')}" if (media.get_attribute('class') != '') else '',
                "id": f"#{media.get_attribute('id')}" if (media.get_attribute('id') != '') else '',
                "autoplay": media.get_attribute('autoplay'),
            }
            css_selector = f"media{properties['id']}{properties['class']}"

            if properties["autoplay"] is None:
                print(f"<Element> == {css_selector}-- has autoplay enabled")

            if media in videos:
                first = "vid1.png"
                second = "vid2.png"
                location = media.location
                size = media.size
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
                    print(f"<Element> == {css_selector}-- has autoplay enabled")
                else:
                    print(f"<Element> -- {css_selector}-- does not have autoplay enabled")

                remove_files(first, second)

        for media in medias:
            if media is not None:
                parent = media
                found = True if (media.get_attribute('controls') is not None) else False
                level = 0
                while (found is False and level < 5):
                    parent = driver.execute_script("return arguments[0].parentNode;", parent)
                    controls = parent.find_elements(By.XPATH, ".//*[contains(@role, 'button') or contains(translate(@class,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'control')] | .//button")
                    for control in controls:
                        print(format_css_selector(driver, control))

    # if control buttons found
                    if len(controls):
                        found = True
                    else:
                        level += 1

            if found:
                print(f"Controls found for Media {format_css_selector(driver, media)}")
            else:
                print(f"No controls found for Media {format_css_selector(driver, media)}")

    else:
        print("No media elements found on page")


def remove_files(firstimg, secimg):
    if os.path.exists(firstimg):
        os.remove(firstimg)
    if os.path.exists(secimg):
        os.remove(secimg)
    print("Removed created files....")
