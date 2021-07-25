import pytest
import datetime

from mock import patch, MagicMock

from doc.gw import generate_queries

def test_simple_fully_identified_query():
  args = {
    "category"  : "cat 1",
    "owner"     : "x",
    "something" : "else"
  }
  results = list(generate_queries(args))
  assert len(results) == 1
  path, args = results[0]
  assert path == "cat 1/owner/x"
  assert len(args) == 1
  assert "something" in args
  assert args["something"] == "else"

def test_unrolling_of_index():
  args = {
    "category"  : "cat 1",
    "something" : "else"
  }
  results = list(generate_queries(args))
  assert len(results) == 1
  path, args = results[0]
  assert path == "cat 1/owner/x"
  assert len(args) == 1
  assert "something" in args
  assert args["something"] == "else"

def test_unrolling_of_categories():
  args = {
    "owner"     : "x",
    "something" : "else"
  }
  results = list(generate_queries(args))
  assert len(results) == 2
  path, args = results[0]
  assert path == "cat 1/owner/x"
  assert len(args) == 1
  assert "something" in args
  assert args["something"] == "else"

  path, args = results[1]
  assert path == "cat 2/owner/x"
  assert len(args) == 1
  assert "something" in args
  assert args["something"] == "else"

def test_determine_category_based_on_type():
  args = {
    "type"      : "type 1",
    "owner"     : "x",
    "something" : "else"
  }
  results = list(generate_queries(args))
  assert len(results) == 1
  path, args = results[0]
  assert path == "cat 1/owner/x"
  assert len(args) == 2
  assert "something" in args
  assert args["something"] == "else"
  assert "type" in args
  assert args["type"] == "type 1"

