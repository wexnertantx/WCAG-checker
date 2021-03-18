import sys

CONSOLE_COLORS = {
  "Windows": {
    "reset": '\033[0m',
    "black": '\033[30m',
    "red": '\033[31m',
    "green": '\033[32m',
    "yellow": '\033[33m',
    "blue": '\033[34m',
    "magenta": '\033[35m',
    "cyan": '\033[36m',
    "white": '\033[37m',
    "bright_black": '\033[90m',
    "bright_red": '\033[91m',
    "bright_green": '\033[92m',
    "bright_yellow": '\033[93m',
    "bright_blue": '\033[94m',
    "bright_magenta": '\033[95m',
    "bright_cyan": '\033[96m',
    "bright_white": '\033[97m',
  },
  "Unix": {
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
}

def get_color_code(color):
  console = 'Windows' if system() == 'Windows' else 'Unix'
  if (color not in CONSOLE_COLORS[console]):
    color = 'reset'
  return CONSOLE_COLORS[console][color]

def print_begin_color(color):
  sys.stdout.write(get_color_code(color))

def print_end_color():
  sys.stdout.write(get_color_code('reset'))

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