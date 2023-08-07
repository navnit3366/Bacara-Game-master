from game import players
from game import cards

def colored (text):
  colors = {
    'r': 31,
    'g': 32,
    'b': 34,
    'c': 36,
    'y': 33,
    'm': 35,
    'w': 37,
    'k': 30,
    'br': 41,
    'bg': 42,
    'bb': 44,
    'bc': 46,
    'by': 43,
    'bm': 45,
    'bw': 47,
    'bk': 40,
    'B': 1,
    'R': 2,
    '0': "0;0",
  }

  for key in colors:
    find = "§" + key
    code = f"\033[{ colors[key] }m"

    text = text.replace(find, code)

  return text


def print_colored (message):
  print(colored(message))


def print_info (message):
  text = f"\n§B§b > {message}§0\n"

  print(colored(text))


def print_success (message):
  text = f"\n§B§g > {message}§0\n"

  print(colored(text))


def print_danger (message):
  text = f"\n§B§y > {message}§0\n"

  print(colored(text))


def print_warn (message):
  text = f"\n§B§r > {message}§0\n"

  print(colored(text))


def get_max_len (list):
  max_len = 0
  for item in list:
    max_len = max(max_len, len(str(item)))

  return max_len


def get_lower_strings (string_list):
  lower_strings = []

  for string in string_list:
    lower_strings.append(string.lower())

  return lower_strings


def has_true (true_list):
  result = False

  for item in true_list:
    if item:
      result = True

  return result