NAME = "Non-text Content"
DESCRIPTION = """All non-text content that is presented to the user has a text alternative
                  that serves the equivalent purpose, except for certain situations"""
LINK = "https://www.w3.org/TR/WCAG21/#non-text-content"
VERSION = 1

def run(driver):
  print(f"Printing title from {NAME}: {driver.title}")
  # do the required tests for this rule
  # return something? maybe number of errors, some percentage, yada yada
  pass