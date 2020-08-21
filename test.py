import re

a = 'dsf92'

b = re.search(r'(?P<RelationVar>\d+)', a)
print (b)
print (b['RelationVar'])