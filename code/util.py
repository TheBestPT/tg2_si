import csv

# Transfrom a csv file to array
def parseCsvToArray(filename):
  reader = csv.reader(
      open(filename, 'r', encoding='utf-8'))
  data = []
  headers = next(reader)
  nextLine = next(reader)
  while nextLine != None:
    obj = {}
    for i in range(len(headers)):
      obj[headers[i]] = nextLine[i]
    data.append(obj)
    try:
      nextLine = next(reader)
    except StopIteration:
      break
    except Exception:
      continue

  return data
