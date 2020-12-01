#!/usr/bin/env python
import sys, getopt, importlib, re, traceback
import drivers

from os import listdir
from os.path import isdir, isfile, join
from selenium.common import exceptions as SeleniumExceptions

LOCAL_RULES_PATH = "rules/local"
EXTERNAL_RULES_PATH = "rules/external"

imported_modules = []

def print_help():
  print("\nusage: main.py [-d | -driver <driver>] <website>")
  print("\navailable drivers:")
  print("\tchrome (default)")
  print("\tfirefox")
  sys.exit()

def import_all_local_rules():
  local_module_path = LOCAL_RULES_PATH.replace('/', '.')
  for rule in listdir(LOCAL_RULES_PATH):
    if (not re.match(r'rule_', rule) or not isdir(join(LOCAL_RULES_PATH, rule))):
      continue

    if (not isfile(join(LOCAL_RULES_PATH, rule, 'main.py'))):
      print(f"Rule {rule} does not have a main.py file!")
      continue

    module = f"{local_module_path}.{rule}.main"
    imported_modules.append(importlib.import_module(module))

def import_all_external_rules():
  # import from external sources (not official)
  # e.g. git? someone made a rule compatible with this module
  # clone the repo into the external folder and import the module into imported_modules
  pass

def run_rules(driver, website):
  try:
    print(f"Initiating the '{driver or ''}' webdriver")
    driver = drivers.get_driver(driver)
    driver.get(website)
    for module in imported_modules:
      try:
        print(f"\nRunning {module.NAME} v{module.VERSION} accessibility rule on '{website}'")
        module.run(driver)
      except Exception as err:
        print(f"\nUncaught error detected in rule {module.NAME}")
        print("Make sure you catch all the exceptions inside the rule itself\n")
        traceback.print_exc(file=sys.stdout)
  except drivers.DriverError as err:
    print("\nDriver error:", err, end='\n')
    print_help()
  except SeleniumExceptions.InvalidArgumentException as err:
    print("\nSelenium driver could not start, please check if the website address is valid")
    print("Error:", err, end='\n')
  except Exception as err:
    print("\nSelenium driver could not start, please check the traceback below to find the reason\n")
    traceback.print_exc(file=sys.stdout)

  if driver != None:
    print("Shutting down the webdriver")
    driver.close()


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hd:", ["driver="])
  except getopt.GetoptError:
    print_help()
    sys.exit(2)
  
  driver = 'chrome'
  for opt, arg in opts:
    if opt == '-h':
      print_help()
    elif opt in ('-d', '--driver'):
      driver = arg

  if len(args) == 0:
    print_help()
  
  # Import all rules
  import_all_local_rules()
  import_all_external_rules()

  # Run all rules
  run_rules(driver, args[0])

main(sys.argv[1:])