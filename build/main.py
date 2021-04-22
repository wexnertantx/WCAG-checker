#!/usr/bin/env python
import sys, getopt, eel, re, traceback

# Custom imports
from util.print import *
import util.process as CS27Process
import util.gui as CS27Gui
import util.rules as CS27Rules

def eel_close(route, websockets):
  if not websockets:
    print('Shutting down the GUI!')
    sys.exit(0)

def eel_start(mode='chrome'):
  eel.start('index.html',
    mode=mode,
    port=8123,
    close_callback=eel_close,
    size=(1800, 1200)
  )


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hd:", ["gui", "driver="])
  except getopt.GetoptError:
    print_help()
    sys.exit(2)
  
  driver = 'chrome'
  for opt, arg in opts:
    if opt == '--gui':
      CS27Gui.start()
      break
    if opt == '-h':
      print_help()
    elif opt in ('-d', '--driver'):
      driver = arg

  if len(args) == 0 and not CS27Gui.is_started():
    print_help()
  
  # Import all rules
  CS27Rules.import_all_local_rules()
  CS27Rules.import_all_external_rules()

  # Run all rules
  if not CS27Gui.is_started():
    CS27Process.analyze_page(driver, args[0])
  else:
    try:
      eel.init('ui/build')
      eel_start()
    except Exception as err:
      if (len(re.findall(r"Chrome", str(err)))):
        print_error('Could not find a Google Chrome installation, retrying with Edge')
        eel_start('edge')
      elif (len(re.findall(r"Edge", str(err)))):
        print_error('Could not find an Edge installation, falling back to browser mode')
        eel_start('browser')
      else:
        print_begin_color('bright_red')
        print("\neel failed to start, check the traceback below to find a reason\n")
        traceback.print_exc(file=sys.stdout)
        print_end_color()

main(sys.argv[1:])
