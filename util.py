import yaml

def load(filename):
  with open(filename) as f:
    return yaml.load(f, Loader=yaml.FullLoader)
