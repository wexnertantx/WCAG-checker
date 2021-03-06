import yaml

config = {}
with open('config.yml', 'r') as file:
  config = yaml.load(file, Loader=yaml.FullLoader)

def get(key):
  if (key):
    if (key not in config):
      print(f"{key} is not a valid config key")
      return None
    
    return config[key]

  return config