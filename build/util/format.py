###
# Returns the element CSS selector as <tag><id><class> format
# @param element      - Selenium WebDriver WebElement
###
def css_selector(driver, element):
  elem_tag = driver.execute_script("return arguments[0].tagName.toLowerCase();", element)
  elem_class = f".{element.get_attribute('class')}" if (element.get_attribute('class') != '') else ''
  elem_id = f"#{element.get_attribute('id')}" if (element.get_attribute('id') != '') else ''
  return f"{elem_tag}{elem_id}{elem_class}"