import logging
logger = logging.getLogger(__name__)

import os
import time

from flask import request, send_from_directory
from flask_restful import Resource

import asyncio
import aiohttp

from baseweb.rest import api

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
  
  util.log2browser(
    "GW",
    "handling document request",
    args
  )
  
  ts = extract_as_list(args, "type")
  if "all" in ts:
    ts.remove("all")
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
      if ts:
        for t in ts:
          args["type"] = t
          yield "{}/list/{}/{}".format(c, index, value), args
      else:
        yield "{}/list/{}/{}".format(c, index, value), args

async def fetch_url(session, path, params):
  base_url = os.environ.get("ARCHIVE_URL", "http://localhost:8000/archive/v1/")
  url = base_url + path + "?" + "&".join([ "{}={}".format(k,v) for k,v in params.items()])
  util.log2browser( "GW", "dispatching archive API query", url)

  response = await session.get(base_url + path, params=params)
  if response.status != 200:
    logger.error("{}".format(url))
    return []
  result = await response.json()
  return result

async def perform_all_queries(args):
  async with aiohttp.ClientSession() as session:
    tasks = []
    for path, params in generate_queries(args):
      task = asyncio.create_task(fetch_url(session, path, params))
      tasks.append(task)
    results = await asyncio.gather(*tasks)
  return [ doc for resultset in results for doc in resultset ]
    
class HandleDocuments(Resource):
  def get(self):
    start = time.time()
    result = asyncio.run(perform_all_queries(request.args.copy()))
    util.log2browser( "GW", "external calls", time.time()-start)
    return result

api.add_resource(HandleDocuments, "/documents")

class HandleRTTTest(Resource):
  def get(self):
    start = time.time()
    util.log2browser( "GW", "external calls", time.time()-start)
    return time.time()-start

api.add_resource(HandleRTTTest, "/rtt")
