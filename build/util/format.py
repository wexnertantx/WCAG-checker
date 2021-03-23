import traceback

# Custom imports
from util.print import *

def getElementTag(driver, element):
  return driver.execute_script("return arguments[0].tagName.toLowerCase();", element)

###
# Returns the element CSS selector as <tag><id><class> format
# @param element      - Selenium WebDriver WebElement
###
def css_selector(driver, element):
  try:
    elem_tag = getElementTag(driver, element)
    elem_class = f".{element.get_attribute('class')}" if (element.get_attribute('class') != '') else ''
    elem_id = f"#{element.get_attribute('id')}" if (element.get_attribute('id') != '') else ''
    return f"{elem_tag}{elem_id}{elem_class}"
  except Exception:
    print_begin_color('bright_red')
    print("\nCSS selector format failed, see stack trace below\n")
    traceback.print_exc(file=sys.stdout)
    print_end_color()
    return f"Unknown HTML element"