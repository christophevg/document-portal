from data import load

documents = load("archive/meta.yaml")

def find_documents(args):
  results = []
  for doc in documents:
    for k, v in args.items():
      if not k in doc or not doc[k] == v:
        continue
      results.append(doc)
  return results
