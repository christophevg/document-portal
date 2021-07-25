import logging
logger = logging.getLogger(__name__)

import os

from flask import request, send_from_directory
from flask_restful import Resource

import requests

from baseweb.rest import api
from baseweb.socketio import socketio

import util

types      = util.load("types.yaml")
mapping    = util.load("mapping.yaml")
categories = mapping["categories"]
indexes    = mapping["indexes"]
acl        = mapping["acl"]

for cat, ts in categories.items():
  for t in ts:
    types[t]["category"] = cat

class HandleMetaTypes(Resource):
  def get(self):
    return types

api.add_resource(HandleMetaTypes, "/meta/types")

def fetch(session, path, params):
  base_url = os.environ.get("ARCHIVE_URL", "http://localhost:8000/archive/search/")
  url = base_url + path + "?" + "&".join([ "{}={}".format(k,v) for k,v in params.items()])
  socketio.emit("log", url)
  with session.get(base_url + path, params=params) as response:
    data = response.json()
    if response.status_code != 200:
      logger.error("{}".format(url))
      return []
    return data

def extract_as_list(args, key, pop=True):
  if pop:
    values = args.pop(key, [])
  else:
    values = args.get(key, [])
  if not type(values) is list:
    values = [ values ]
  return values

def generate_queries(args):
  """
  given a set of arguments, generate query paths including category and index
  """
  ts = extract_as_list(args, "type")
  if "all" in ts:
    ts.remove("all")
  if ts:
    args["type"] = ts
  cats = extract_as_list(args, "category")
  
  if not cats:
    # determine category/ies depending on types (if provided)
    if ts:
      # only include cats for required
      cats = { types[t]["category"] : True for t in ts }.keys()
    else:
      # full archive scan ;-)
      cats = categories.keys()
     
  # step 2 : determine best index for each category
  for c in cats:
    index        = None
    index_values = []
    for i in indexes[c]:
      if i in args:
        index = i
        index_values = extract_as_list(args, index)
        break
    if index is None:
      # no indexed value included in args => unroll to all possible index values
      # for preferred (first) index
      index = indexes[c][0]
      # TODO implement actual acl provider
      index_values = acl["x"][index]

    for value in index_values:
      yield "{}/{}/{}".format(c, index, value), args
      
class HandleDocuments(Resource):
  def get(self):
    results = []
    # TODO make async
    with requests.Session() as session:
      for path, params in generate_queries(request.args.copy()):
        results += fetch(session, path, params)
    return results

api.add_resource(HandleDocuments, "/documents")
