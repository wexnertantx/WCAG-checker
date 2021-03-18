#!/usr/bin/env python
import sys, getopt, importlib, re, traceback
import drivers

from os import listdir
from os.path import isdir, isfile, join
from selenium.common import exceptions as SeleniumExceptions
from util.print import *

LOCAL_RULES_PATH = "rules/local"
EXTERNAL_RULES_PATH = "rules/external"

imported_modules = []

def import_all_local_rules():
  local_module_path = LOCAL_RULES_PATH.replace('/', '.')
  for rule in listdir(LOCAL_RULES_PATH):
    if (not re.match(r'rule_', rule) or not isdir(join(LOCAL_RULES_PATH, rule))):
      continue

    if (not isfile(join(LOCAL_RULES_PATH, rule, 'main.py'))):
      print_error(f"Rule {rule} does not have a main.py file!")
      continue

    module = f"{local_module_path}.{rule}.main"
    imported_modules.append(importlib.import_module(module))

def import_all_external_rules():
  # import from external sources (not official)
  # e.g. git? someone made a rule compatible with this module
  # clone the repo into the external folder and import the module into imported_modules
  pass

def run_rules(driver_name, website):
  driver = None
  try:
    print_info(f"Initiating the '{driver_name or ''}' webdriver")
    driver = drivers.get_driver(driver_name)
    print_success(f"'{driver_name}' driver loaded successfully! Loading website '{website}'")
    driver.get(website)
    print_success(f"'{website}' loaded successfully! Running accessibility rules")
    for module in imported_modules:
      try:
        print_info(f"\nRunning {module.NAME} v{module.VERSION} accessibility rule on '{website}'")
        module.run(driver)
      except Exception as err:
        print_begin_color('bright_red')
        print(f"Uncaught error detected in rule {module.NAME}")
        print("Make sure you catch all the exceptions inside the rule itself}\n")
        traceback.print_exc(file=sys.stdout)
        print_end_color()
  except drivers.DriverError as err:
    print_error("\nDriver error:", err, end='\n')
  except SeleniumExceptions.InvalidArgumentException as err:
    print_error("\nSelenium driver could not start, please check if the website address is valid")
    print_error("Error:", err, end='\n')
  except Exception as err:
    print_begin_color('bright_red')
    print("\nSelenium driver could not start, please check the traceback below to find the reason\n")
    traceback.print_exc(file=sys.stdout)
    print_end_color()

  if driver != None:
    print_info("\nShutting down the webdriver")
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