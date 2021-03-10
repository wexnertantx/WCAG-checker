from platform import system
from os import path, getcwd, mkdir, chmod

from selenium import webdriver

class DriverError(Exception):
  pass

def get_driver(driver_name="chrome"):
  drivers = {
    "chrome": {
      "file": "chromedriver",
      "init": webdriver.Chrome,
      "options": webdriver.ChromeOptions
    },
    "firefox": {
      "file": "geckodriver",
      "init": webdriver.Firefox,
      "options": webdriver.FirefoxOptions
    },
    # 'edge': '',
    # 'safari': '',
  }

  if driver_name not in drivers:
    raise DriverError("Invalid driver specified!")

  driver_options = drivers[driver_name]["options"]()
  driver_file = drivers[driver_name]["file"]  
  driver_exec = f"{driver_file}.exe"
  if (system() != 'Windows'):
    driver_exec = f"{driver_file}_{system().lower()}"
  
  driver_options.add_argument('--headless')
  driver_options.add_argument('--use-fake-ui-for-media-stream')

  driver_path = path.join(getcwd(), 'drivers', driver_name)
  driver_logs_path = path.join(driver_path, 'logs')
  if (not path.exists(driver_logs_path)):
    mkdir(driver_logs_path, mode=0o777)

  driver_logs_file_path = path.join(driver_logs_path, f"{driver_file}.log")
  driver_exec_file_path = path.join(driver_path, driver_exec)
  
  return drivers[driver_name]["init"](executable_path=driver_exec_file_path, service_log_path=driver_logs_file_path, options=driver_options)
