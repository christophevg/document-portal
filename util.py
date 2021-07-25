import yaml

def load(filename):
  with open(filename) as f:
    return yaml.load(f, Loader=yaml.FullLoader)



from baseweb.socketio import socketio

def log2browser(reporter, message, arguments=None):
  socketio.emit("log", {
    "reporter"  : reporter,
    "message"   : message,
    "arguments" : arguments
  });
