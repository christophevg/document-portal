import logging
logger = logging.getLogger(__name__)

import os

from flask import request, send_from_directory
from flask_restful import Resource

from baseweb.rest import api

from data.meta      import types
from data.documents import find_documents

class HandleMetaTypes(Resource):
  def get(self):
    return types

api.add_resource(HandleMetaTypes, "/meta/types")

class HandleDocuments(Resource):
  def get(self, guid=None):
    if not guid is None:
      return send_from_directory(os.path.join(os.getcwd(), 'archive'), guid + ".pdf")
    return find_documents(request.args)

api.add_resource(HandleDocuments, "/documents", "/documents/<string:guid>")
