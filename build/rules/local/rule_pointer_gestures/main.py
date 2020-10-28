NAME = "Pointer Gestures"
DESCRIPTION = """All functionality that uses multipoint or path-based gestures for operation 
                  can be operated with a single pointer without a path-based gesture, 
                  unless a multipoint or path-based gesture is essential."""
LINK = "https://www.w3.org/TR/WCAG21/#pointer-gestures"
VERSION = 1

def run(driver):
  print(f"Printing title from {NAME}: {driver.title}")
  # do the required tests for this rule
  # return something? maybe number of errors, some percentage, yada yada
  pass