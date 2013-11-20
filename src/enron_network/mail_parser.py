# Parses each file from the Enron email dataset and produces a tab separated
# From and To email address tuples. Multiple recipients in the To: header are
# written out as multiple lines of output.
import email.parser
import os
import re
import sys

def remove_special_chars(s):
  return re.sub(r"[<>\"' ]", "", s)

fname = sys.argv[1]
if os.path.isfile(fname) and fname.endswith("."):
  fin = open(sys.argv[1], 'rb')
  parser = email.parser.HeaderParser()
  msg = parser.parse(fin, headersonly=True)
  fin.close()
  try:
    from_value = msg["From"]
    to_values = msg["To"].replace("\r\n", "").replace("\t", "").split(", ")
    if from_value != None and to_values != None:
      from_value = remove_special_chars(from_value)
      for to_value in to_values:
        to_value = remove_special_chars(to_value)
        print("%s\t%s" % (from_value, to_value))
  except AttributeError:
    pass
