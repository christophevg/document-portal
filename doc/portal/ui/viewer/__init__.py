import logging
logger = logging.getLogger(__name__)

import os

from baseweb.interface import register_component

register_component("viewer.js", os.path.dirname(__file__))
