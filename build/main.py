#!/usr/bin/env python
import sys, getopt, importlib, re, traceback
import drivers

from os import listdir
from os.path import isdir, isfile, join
from selenium.common import exceptions as SeleniumExceptions

LOCAL_RULES_PATH = "rules/local"
EXTERNAL_RULES_PATH = "rules/external"

imported_modules = []

COLORS = {
  "reset": '\u001b[0m',
  "black": '\u001b[30m',
  "red": '\u001b[31m',
  "green": '\u001b[32m',
  "yellow": '\u001b[33m',
  "blue": '\u001b[34m',
  "magenta": '\u001b[35m',
  "cyan": '\u001b[36m',
  "white": '\u001b[37m',
  "bright_black": '\u001b[30;1m',
  "bright_red": '\u001b[31;1m',
  "bright_green": '\u001b[32;1m',
  "bright_yellow": '\u001b[33;1m',
  "bright_blue": '\u001b[34;1m',
  "bright_magenta": '\u001b[35;1m',
  "bright_cyan": '\u001b[36;1m',
  "bright_white": '\u001b[37;1m',
}
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


      


def print_begin_color(color):
  sys.stdout.write(COLORS[color] if color in COLORS else COLORS['reset'])

def print_end_color():
  sys.stdout.write("\u001b[0m")

def print_color(*args, color='reset', **kwargs):
  print_begin_color(color)
  print(*args, **kwargs)
  print_end_color()

def print_error(*args, **kwargs):
  print_color(*args, **kwargs, color="bright_red")

def print_info(*args, **kwargs):
  print_color(*args, **kwargs, color="cyan")

def print_success(*args, **kwargs):
  print_color(*args, **kwargs, color="bright_green")

def print_help():
  print_begin_color('bright_yellow')
  print("usage: main.py [-d | -driver <driver>] <website>")
  print("\navailable drivers:")
  print("\tchrome (default)")
  print("\tfirefox")
  print_end_color()
  sys.exit()

def print_results(resultpercent,modstr):
  if float(resultpercent)>50:
    print_success(f"{resultpercent}{modstr}")
  elif float(resultpercent<50):
    print_error(f"{resultpercent}{modstr}")
  elif resultpercent==-1:
    print_error(f"{modstr}")
  else:
    print("")

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
  try:
    print_info(f"Initiating the '{driver_name or ''}' webdriver")
    driver = drivers.get_driver(driver_name)
    print_success(f"'{driver_name}' driver loaded successfully! Loading website '{website}'")
    driver.get(website)
    print_success(f"'{website}' loaded successfully! Running accessibility rules")
    for module in imported_modules:
      try:
        print_info(f"\nRunning {module.NAME} v{module.VERSION} accessibility rule on '{website}'")
        try:
          result_percentage,result_string = module.run(driver)
          print_results(result_percentage,result_string)
        except Exception as err:
          print("No output for this module")
      except Exception as err:
        print_begin_color('bright_red')
        print(f"Uncaught error detected in rule {module.NAME}")
        print("Make sure you catch all the exceptions inside the rule itself}\n")
        traceback.print_exc(file=sys.stdout)
        print_end_color()
  except drivers.DriverError as err:
    print_error("\nDriver error:", err, end='\n')
    print_help()
  except SeleniumExceptions.InvalidArgumentException as err:
    print_error("\nSelenium driver could not start, please check if the website address is valid")
    print_error("Error:", err, end='\n')
  except Exception as err:
    print_begin_color('bright_red')
    print("\nSelenium driver could not start, please check the traceback below to find the reason\n")
    traceback.print_exc(file=sys.stdout)
    print_begin_end()

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