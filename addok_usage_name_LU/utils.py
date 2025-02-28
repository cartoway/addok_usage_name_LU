import re

black = ['à', 'di', 'au', 'aux', 'des', 'l', 'sous', 'et', 'du', 'les', 'd', 'lès', 'la', 'le', 'en', 'de', 'sur', 'saint', 'sainte',
# Luxembourg
# -- nothing
]

# Adelans-et-le-Val-de-Bithaine -> Adelans-et-le-Val-de-Bithaine, adelans-et-le-val, adelans
# Return full name first
def subpart_generator(name):
  if '-' not in name:
    return (name,)

  s = name.lower().replace('\'', ' ').split('-')
  l = map(lambda i: s[i] not in black and not s[i][0].isdigit() and '-'.join(s[0:i+1]), range(len(s)-2, -1, -1))
  l = list(filter(lambda i: i, l))
  if len(l) > 0:
    l.insert(0, name)
    return l
  else:
    return (name,)


def make_labels(helper, result):
  if result.labels:
    return

  ret = []
  for city in subpart_generator(result.city):
    for name in (result.name if isinstance(result.name, (tuple, list)) else [result.name]):
      # Most complet first
      if result.type == 'municipality':
        ret.extend(([result.postcode, city], [city, result.postcode], [result.postcode], [city]))
      elif result.type in ['street', 'locality']:
        ret.extend(([name, result.postcode, city], [name, city, result.postcode], [name, result.postcode], [name, city]))
      elif result.type == 'housenumber':
        # prepend house number
        ret.extend(([result.housenumber, name, result.postcode, city], [result.housenumber, name, city, result.postcode], [result.housenumber, name, result.postcode], [result.housenumber, name, city]))
        # append house number
        ret.extend(([name, result.housenumber, result.postcode, city], [name, result.housenumber, city, result.postcode], [name, result.housenumber, result.postcode], [name, result.housenumber, city]))

  result.labels.extend(list(map(lambda a: ' '.join(a), ret)))
