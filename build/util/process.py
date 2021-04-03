#!/usr/bin/env python
import sys, eel, traceback, threading

from selenium.common import exceptions as SeleniumExceptions

# Custom imports
import drivers as CS27Driver
from util.print import *
import util.errors as CS27Exceptions
import util.gui as CS27Gui
import util.rules as CS27Rules

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
    threading.Thread(target=analyze_page, args=('chrome', website)).start()
  else:
    set_process_state(PROCESS_STATES['RUNNING'])

@eel.expose
def eel_pause_process():
  set_process_state(PROCESS_STATES['PAUSED'])

@eel.expose
def eel_stop_process():
  set_process_state(PROCESS_STATES['STOPPED'])
### End of eel bridge functions

def set_process_state(state):
  global process_state
  process_state = state

def pause_process():
  global process_state
  while (process_state == PROCESS_STATES['PAUSED']):
    pass

  if (process_state == PROCESS_STATES['RUNNING']):
    CS27Gui.run_eel('send_python_action_finish_event')() # Send event to let UI know that the resume process action is successful
    print_info(f"The process has been resumed!")

def analyze_page(driver_name, website):
  set_process_state(PROCESS_STATES['RUNNING'])
  driver = None
  try:
    print_info(f"Initiating the '{driver_name or ''}' webdriver")
    driver = CS27Driver.get_driver(driver_name)
    print_success(f"'{driver_name}' driver loaded successfully! Loading website '{website}'")
    driver.get(website)
    print_success(f"'{website}' loaded successfully! Running accessibility rules")
    CS27Gui.run_eel('send_python_action_finish_event')() # Send event to let UI know that the start process action is successful
    for rule in CS27Rules.get_rules():
      try:
        if (process_state == PROCESS_STATES['PAUSED']):
          print_info(f"The process has been paused!")
          CS27Gui.run_eel('send_python_action_finish_event')() # Send event to let UI know that the pause process action is successful
          pause_process()

        if (process_state == PROCESS_STATES['STOPPED']):
          print_info(f"The process has been forcibly stopped!")
          CS27Gui.run_eel('send_python_action_finish_event')() # Send event to let UI know that the stop process action is successful
          break

        print_info(f"\nRunning {rule.NAME} v{rule.VERSION} accessibility rule on '{website}'")
        if (CS27Rules.is_rule_disabled(rule.ID)):
          raise CS27Exceptions.NoResult("This rule is disabled!")

        CS27Gui.run_eel('send_rule_state_change_event')(rule.ID, CS27Rules.RULE_STATES['RUNNING'])
        result_percentage, result_string = rule.run(driver)
        print_results(result_percentage, result_string)
        CS27Gui.run_eel('send_rule_state_change_event')(rule.ID, CS27Rules.RULE_STATES['FINISHED'])
      except CS27Exceptions.NoResult as err:
        print_error(err)
        CS27Gui.run_eel('send_rule_state_change_event')(rule.ID, CS27Rules.RULE_STATES['DISABLED'])
      except Exception as err:
        print_begin_color('bright_red')
        print(f"[Error] {rule.NAME} rule failed execution:", err, '\n')
        traceback.print_exc(file=sys.stdout)
        print_end_color()
        CS27Gui.run_eel('send_rule_state_change_event')(rule.ID, CS27Rules.RULE_STATES['FAILED'])
  except CS27Driver.DriverError as err:
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

  set_process_state(PROCESS_STATES['STOPPED'])
  CS27Gui.run_eel('send_process_finish_event')()