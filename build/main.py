#!/usr/bin/env python
from os import listdir
from os.path import isdir, isfile, join
import importlib
import re
import selenium

import drivers, config

LOCAL_RULES_PATH = "rules/local"
EXTERNAL_RULES_PATH = "rules/external"

imported_modules = []

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

import_all_local_rules()
import_all_external_rules()

def run_rules(website):
  print("Initiating the webdriver")
  driver = drivers.get_driver()
  try:
    driver.get(website)
    for module in imported_modules:
      print(f"\nRunning {module.NAME} v{module.VERSION} accessibility rule on '{website}'")
      module.run(driver)
  except Exception as e:
    raise e
  finally:
    print("Shutting down the webdriver")
    driver.close()

run_rules(config.get('website'))