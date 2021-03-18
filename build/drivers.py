import re
from platform import system
from os import path, getcwd, mkdir, chmod, listdir, rename
# Modules required to download and unzip the drivers
from urllib import request
from shutil import rmtree
from zipfile import ZipFile

from selenium import webdriver

drivers = {
  "chrome": {
    "file": "chromedriver",
    "init": webdriver.Chrome,
    "options": webdriver.ChromeOptions,
    "suffix": {
      "Windows": "win32",
      "Linux": "linux64",
      "Darwin": "mac64",
    }
  },
  "firefox": {
    "file": "geckodriver",
    "init": webdriver.Firefox,
    "options": webdriver.FirefoxOptions
  },
  # 'edge': '',
  # 'safari': '',
}

driver = {
  "name": None,
  "options": None,
  "exe_name": None,
  "exe_path": None,

}

class DriverError(Exception):
  pass

def download_drivers(driver_name):
  wbdrv_dir = path.join(getcwd(), 'drivers')
  if (not path.exists(wbdrv_dir)):
    mkdir(wbdrv_dir, mode=0o777)

  wbdrv_name_dir = path.join(wbdrv_dir, driver_name)
  if (not path.exists(wbdrv_name_dir)):
    mkdir(wbdrv_name_dir, mode=0o777)
    
  if (driver_name == 'chrome'):
    with request.urlopen('https://chromedriver.storage.googleapis.com/LATEST_RELEASE') as response:
      version = response.read().decode()
      major_version = version.split('.')[0]
      version_dir = path.join(wbdrv_name_dir, f'v{major_version}')
      version_exe_path = path.join(version_dir, driver["exe_name"])

      if (not path.exists(version_dir)):
        mkdir(version_dir, mode=0o777)

      if (path.isfile(version_exe_path)):
        raise DriverError(f'Browser version mismatch! Make sure your browser is updated to the latest stable version v{version}')

      download_dir = path.join(wbdrv_dir, 'temp')
      if (path.exists(download_dir)):
        rmtree(download_dir)
      mkdir(download_dir, mode=0o777)

      driver_suffix = drivers[driver_name]["suffix"][system()]
      driver_zipfile = f'{download_dir}/chromedriver_{driver_suffix}.zip'
      print(f'Downloading chromedriver_{driver_suffix}.zip into {download_dir}')
      request.urlretrieve(f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_{driver_suffix}.zip', driver_zipfile)

      print(f'Extracting chromedriver_{driver_suffix}.zip v{version} into {version_dir}')
      with ZipFile(driver_zipfile) as zipfile:
        zipfile.extractall(version_dir)
        rename(f'{version_dir}/chromedriver', f'{version_dir}/{driver["exe_name"]}')

      rmtree(download_dir)

# def get_version_via_shell():
  # cmds = {
  #   "Windows": [
  #     'wmic datafile where name="C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe" get Version /value',
  #     'wmic datafile where name="C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe" get Version /value',
  #   ],
  #   "Linux": [
  #     'google-chrome --version',
  #   ],
  #   "Darwin": [
  #     'google-chrome --version',
  #   ]
  # }

  # if (system() == 'Windows'):
    

  # for cmd in cmds[system()]:
  #   proc = subprocess.Popen(
  #     cmd,
  #     shell=True,
  #     stdin=subprocess.PIPE,
  #     stdout=subprocess.PIPE,
  #   )
  #   out, err = proc.communicate()
  #   decoded = re.sub(r'[\r\n]', '', out.decode())
  #   split_for_os = decoded.split('=') if system() == 'Windows' else decoded.split(' ')
  #   print(split_for_os)
  #   # if (system() == 'Windows' and decoded[0] == 'Version'):
  #   #   print(decoded[1][0:2])
  #   # if (system() == 'Linux'):


def get_driver(driver_name="chrome"):
  if driver_name not in drivers:
    raise DriverError("Invalid driver specified!")
  
  driver["name"] = driver_name
  driver["options"] = drivers[driver_name]["options"]()
  driver_file = drivers[driver_name]["file"]
  driver["exe_name"] = f"{driver_file}.exe"
  if (system() != 'Windows'):
    driver["exe_name"] = f"{driver_file}_{system().lower()}"
  
  driver["options"].add_argument('--headless')
  driver["options"].add_argument('--use-fake-ui-for-media-stream')

  # driver_logs_path = path.join(getcwd(), 'logs')
  # if (not path.exists(driver_logs_path)):
  #   mkdir(driver_logs_path, mode=0o777)
  # driver_logs_file_path = path.join(driver_logs_path, f"{driver_file}.log")

  driver_versions_path = path.join(getcwd(), 'drivers', driver_name)
  driver_versions = listdir(driver_versions_path)
  driver_versions.reverse()
  wbdrv = None
  for version in driver_versions:
    version_path = path.join(driver_versions_path, version)
    driver["exe_path"] = path.join(version_path, driver["exe_name"])

    if (not path.isfile(driver["exe_path"])):
      continue
    
    try:
      wbdrv = drivers[driver_name]["init"](executable_path=driver["exe_path"], options=driver["options"])
    except Exception as e:
      wbdrv = None  

  if (not wbdrv):
    download_drivers(driver_name)
    return get_driver(driver_name)

  return wbdrv
  
    # print(wbdr.capabilities['browserVersion'])
    # print(wbdr.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
