import yaml, json, eel

CONFIG_FILE = 'config.yml'

config = {}
with open(CONFIG_FILE, 'r') as f:
  config = yaml.load(f, Loader=yaml.FullLoader)

def get(key):
  if (key):
    if (key not in config):
      print(f"{key} is not a valid config key")
      return None
    
    return config[key]

  return config

@eel.expose
def eel_save_config(data, key=None):
  data = json.loads(data)
  if key != None:
    config[key] = data
  else:
    config = data
  
  yaml_str = yaml.dump(config, default_flow_style=False)
  with open(CONFIG_FILE, 'w') as f:
    f.write(yaml_str)

@eel.expose
def eel_load_config(key=None):
  if key != None:
    json_str = json.dumps(config[key])
  else:
    json_str = json.dumps(config)
  
  return json_str
    