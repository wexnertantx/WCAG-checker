#!/usr/bin/env python
import importlib, re, eel
from os import listdir
from os.path import isdir, isfile, join

import config
import util.process as CS27Process

RULE_STATES = {
  'FAILED': -2,
  'DISABLED': -1,
  'PENDING': 0,
  'RUNNING': 1,
  'FINISHED': 2,
}

LOCAL_PATH = "rules/local"
EXTERNAL_PATH = "rules/external"

rules_list = []

def import_all_local_rules():
  local_module_path = LOCAL_PATH.replace('/', '.')
  for rule in listdir(LOCAL_PATH):
    if (not re.match(r'rule_', rule) or not isdir(join(LOCAL_PATH, rule))):
      continue

    if (not isfile(join(LOCAL_PATH, rule, 'main.py'))):
      print_error(f"Rule {rule} does not have a main.py file!")
      continue

    module = f"{local_module_path}.{rule}.main"
    rules_list.append(importlib.import_module(module))

def import_all_external_rules():
  # import from external sources (not official)
  # e.g. git? someone made a rule compatible with this module
  # clone the repo into the external folder and import the module into rules_list
  pass

def is_rule_disabled(rule):
  rules_config = config.get('rules')
  return (
    (
      ("local" in rules_config) and
      ("disabled" in rules_config["local"]) and
      (rules_config["local"]["disabled"] != None) and
      (rule in rules_config["local"]["disabled"])
    ) or (
      ("external" in rules_config) and
      ("disabled" in rules_config["external"]) and
      (rules_config["external"]["disabled"] != None) and
      (rule in rules_config["external"]["disabled"])
    )
  )

def is_local_rule(rule_path):
  if "local" in rule_path:
    return True
  return False

def get_rules():
  return rules_list

@eel.expose
def eel_request_rules():
  rules = []
  for rule in get_rules():
    rules.append({
      "id": rule.ID,
      "name": rule.NAME,
      "description": rule.DESCRIPTION,
      "version": rule.VERSION,
      "link": rule.LINK,
      "disabled": is_rule_disabled(rule.ID),
      "local": is_local_rule(rule.SCRIPT_DIR)
    })  
  return rules