#!/usr/bin/env python
import sys, getopt, importlib, re, traceback, eel, threading

from os import listdir, path
from os.path import isdir, isfile, join
from selenium.common import exceptions as SeleniumExceptions

# Custom imports
import drivers, config
from util.print import *
import util.errors as CS27Exceptions

PROCESS_STATES = {
  'STOPPED': -1,
  'PAUSED': 0,
  'RUNNING': 1,
}
process_state = PROCESS_STATES['STOPPED']

### eel bridge functions
@eel.expose
def eel_start_process(website):
  global process_state
  if process_state == PROCESS_STATES['STOPPED']:
    threading.Thread(target=run_rules, args=('chrome', website)).start()
  else:
    process_state = PROCESS_STATES['RUNNING']

@eel.expose
def eel_pause_process():
  global process_state
  process_state = PROCESS_STATES['PAUSED']

@eel.expose
def eel_stop_process():
  global process_state
  process_state = PROCESS_STATES['STOPPED']
### End of eel bridge functions

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

def is_rule_disabled(rule):
  rules_config = config.get('rules')
  return (
    (
      ("internal" in rules_config) and
      ("disabled" in rules_config["internal"]) and
      (rules_config["internal"]["disabled"] != None) and
      (rule in rules_config["internal"]["disabled"])
    ) or (
      ("external" in rules_config) and
      ("disabled" in rules_config["external"]) and
      (rules_config["external"]["disabled"] != None) and
      (rule in rules_config["external"]["disabled"])
    )
  )

def pause_process():
  global process_state
  while (process_state == PROCESS_STATES['PAUSED']):
    pass

  if (process_state == PROCESS_STATES['RUNNING']):
    print_info(f"The process has been resumed!")

def run_rules(driver_name, website):
  global process_state
  driver = None
  process_state = PROCESS_STATES['RUNNING']
  try:
    print_info(f"Initiating the '{driver_name or ''}' webdriver")
    driver = drivers.get_driver(driver_name)
    print_success(f"'{driver_name}' driver loaded successfully! Loading website '{website}'")
    driver.get(website)
    print_success(f"'{website}' loaded successfully! Running accessibility rules")
    for rule in imported_modules:
      try:
        if (process_state == PROCESS_STATES['PAUSED']):
          print_info(f"The process has been paused!")
          pause_process()

        if (process_state == PROCESS_STATES['STOPPED']):
          print_info(f"The process has been forcibly stopped!")
          eel.finish_action_js()
          break

        print_info(f"\nRunning {rule.NAME} v{rule.VERSION} accessibility rule on '{website}'")
        result_percentage, result_string = rule.run(driver)
        print_results(result_percentage, result_string)
      except CS27Exceptions.NoResult as err:
        print_error(err)
      except Exception as err:
        print_begin_color('bright_red')
        print(f"Leaked error detected in rule {module.NAME}")
        print("Make sure you catch all the exceptions inside the rule itself}\n")
        traceback.print_exc(file=sys.stdout)
        print_end_color()
      finally:
        print(rule.ID)
        eel.finish_rule_js(rule.ID)
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

  process_state = PROCESS_STATES['STOPPED']
  eel.finish_process_js()

def eel_close(route, websockets):
  if not websockets:
    print('Shutting down the GUI!')
    sys.exit(0)

@eel.expose
def eel_request_rules():
  rules = []
  for rule in imported_modules:
    rules.append({
      "id": rule.ID,
      "name": rule.NAME,
      "description": rule.DESCRIPTION,
      "version": rule.VERSION,
      "link": rule.LINK,
      "disabled": is_rule_disabled(rule.ID)
    })  
  return rules

def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hd:", ["gui", "driver="])
  except getopt.GetoptError:
    print_help()
    sys.exit(2)
  
  driver = 'chrome'
  in_gui = False
  for opt, arg in opts:
    if opt == '--gui':
      in_gui = True
      break
    if opt == '-h':
      print_help()
    elif opt in ('-d', '--driver'):
      driver = arg

  if len(args) == 0 and not in_gui:
    print_help()
  
  # Import all rules
  import_all_local_rules()
  import_all_external_rules()

  # Run all rules
  if not in_gui:
    run_rules(driver, args[0])
  else:
    eel.init('ui/dist')
    eel.start('index.html', port=8123, close_callback=eel_close)

main(sys.argv[1:])
