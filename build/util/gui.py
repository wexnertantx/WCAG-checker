#!/usr/bin/env python
import eel

STARTED = False

def is_started():
  return STARTED

def start():
  global STARTED
  STARTED = True

def run_eel(eel_fn):
  if (is_started()):
    return getattr(eel, eel_fn)

  return lambda *args: None