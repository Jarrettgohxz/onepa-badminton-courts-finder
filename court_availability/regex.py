import re

match = re.search(re.compile(r'(?:\w*)(\d)', re.I),
                  '2'.replace(' ', ''))


# match = re.search(re.compile(r'(\w*)', re.I),
#                   'Badminton 2')

if match != None:
    print(match.groups())


# match = re.match(re.compile(r'(\w|\s)*', re.I), 'Badminton ')
# print(match)
