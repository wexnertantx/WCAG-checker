import sys
import re
from platform import system
from os import path, getcwd, mkdir, chmod, listdir, rename
# Modules required to download and unzip the drivers
from urllib import request
from shutil import rmtree
from zipfile import ZipFile
import tarfile

from selenium import webdriver

drivers = {
  "chrome": {
    "file": "chromedriver",
    "init": webdriver.Chrome,
    "options": webdriver.ChromeOptions,
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

class VersionMismatchError(Exception):
  pass

class DriverError(Exception):
  pass

def create_driver_directory(driver_name):
  wbdrv_dir, wbdrv_name_dir = get_driver_directory(driver_name)
  if (not path.exists(wbdrv_dir)):
    mkdir(wbdrv_dir, mode=0o777)
  if (not path.exists(wbdrv_name_dir)):
    mkdir(wbdrv_name_dir, mode=0o777)

def create_logs_directory():
  wbdrv_logs_dir = path.join(getcwd(), 'drivers', 'logs')
  if (not path.exists(wbdrv_logs_dir)):
    mkdir(wbdrv_logs_dir, mode=0o777)

  return wbdrv_logs_dir

def get_driver_directory(driver_name):
  wbdrv_dir = path.join(getcwd(), 'drivers')
  wbdrv_name_dir = path.join(wbdrv_dir, driver_name)
  return wbdrv_dir, wbdrv_name_dir

def download_drivers(driver_name):
  wbdrv_dir, wbdrv_name_dir = get_driver_directory(driver_name)
  if (driver_name == 'chrome'):
    with request.urlopen('https://chromedriver.storage.googleapis.com/LATEST_RELEASE') as response:
      version = response.read().decode()
      major_version = version.split('.')[0]
      version_dir = path.join(wbdrv_name_dir, f'v{major_version}')
      version_exe_path = path.join(version_dir, driver["exe_name"])
  elif (driver_name == 'firefox'):
    with request.urlopen('https://github.com/mozilla/geckodriver/releases/latest') as response:
      content = response.read().decode()
      version = re.findall(r"<title>(?:.*?)(\d+\.\d+\.\d+)(?:.*?)<\/title>", content)[0]
      version_dir = path.join(wbdrv_name_dir, f'v{version}')
      version_exe_path = path.join(version_dir, driver["exe_name"])

  if (not path.exists(version_dir)):
    mkdir(version_dir, mode=0o777)

  if (path.isfile(version_exe_path)):
    raise DriverError(f'Browser version mismatch! Make sure your browser is updated to the latest stable version v{version}')

  download_dir = path.join(wbdrv_dir, 'temp')
  if (path.exists(download_dir)):
    rmtree(download_dir)
  mkdir(download_dir, mode=0o777)

  if (driver_name == 'chrome'):
    platforms = {
      "Windows": "win32",
      "Linux": "linux64",
      "Darwin": "mac64",
    }
    platform = platforms[system()]

    print(f'Downloading latest chromedriver version into {download_dir}')
    archive_name = f'chromedriver_{platform}'
    archive_ext = 'zip'
    archive_file, header = request.urlretrieve(f'https://chromedriver.storage.googleapis.com/{version}/{archive_name}.{archive_ext}')
  elif (driver_name == 'firefox'):
    platforms = {
      "Windows": "win32",
      "Linux": "linux64",
      "Darwin": "macos",
    }
    platform = platforms[system()]

    print(f'Downloading latest geckodriver version into {download_dir}')
    archive_name = f'geckodriver-v{version}-{platform}'
    archive_ext = 'zip' if system() == 'Windows' else 'tar.gz'
    archive_file, header = request.urlretrieve(f'https://github.com/mozilla/geckodriver/releases/download/v{version}/{archive_name}.{archive_ext}')

  print(f'Extracting {archive_name} v{version} archive "{archive_file}" into "{version_dir}"')
  if archive_ext == 'zip':
    with ZipFile(archive_file) as zipfile:
      zipfile.extractall(version_dir)
  else:
    with tarfile.open(archive_file) as tarball:
      tarball.extractall(version_dir)

  if (system() != 'Windows'):
    rename(path.join(version_dir, drivers[driver_name]["file"]), path.join(version_dir, driver["exe_name"]))

  rmtree(download_dir)

def get_driver(driver_name="chrome"):
  if driver_name not in drivers:
    raise DriverError("Invalid driver specified!")

  create_driver_directory(driver_name)
  
  driver["name"] = driver_name
  driver["options"] = drivers[driver_name]["options"]()
  driver_file = drivers[driver_name]["file"]
  driver["exe_name"] = f"{driver_file}.exe"
  if (system() != 'Windows'):
    driver["exe_name"] = f"{driver_file}_{system().lower()}"
  
  driver["options"].add_argument('--headless')
  driver["options"].add_argument('--use-fake-ui-for-media-stream')

  wbdrv_logs_dir = create_logs_directory()
  wbdrv_logs_file_path = path.join(wbdrv_logs_dir, f"{driver_file}.log")

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
      wbdrv = drivers[driver_name]["init"](executable_path=driver["exe_path"], options=driver["options"], service_log_path=wbdrv_logs_file_path)
      break
    except Exception as e:
      wbdrv = None
      err_match = re.findall(r"moz:firefoxOptions.binary", str(e))
      if (len(err_match)):
        raise DriverError("Firefox binary could not be found. Make sure that firefox is installed in the default location")
      else:
        raise DriverError(e)

  if (not wbdrv):
    download_drivers(driver_name)
    return get_driver(driver_name)

  return wbdrv
  


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


  # print(wbdr.capabilities['browserVersion'])
  # print(wbdr.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
