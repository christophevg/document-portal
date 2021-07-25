import logging
logger = logging.getLogger(__name__)

import os

from flask import request, send_from_directory
from flask_restful import Resource

from baseweb.rest import api

import util

PATH = os.path.dirname(os.path.realpath(__file__))
META = os.path.join(PATH, "meta.yaml")
documents = util.load(META)

def find_documents(args):
  results = []
  for doc in documents:
    if all( [ not k in doc or doc[k] == v for k, v in args.items() ] ):
      results.append(doc)
  return results

class HandleSearch(Resource):
  def get(self, category, index_name, index_value):
    args = request.args.copy()
    args["category"] = category
    args[index_name] = index_value
    return find_documents(args)

api.add_resource(HandleSearch, "/archive/search/<string:category>/<string:index_name>/<string:index_value>")

class HandleDocument(Resource):
  def get(self, guid):
    return send_from_directory(PATH, guid + ".pdf")

api.add_resource(HandleDocument, "/archive/document/<string:guid>")
