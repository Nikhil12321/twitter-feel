import re

expr = r'(.)\1{3,}'
replace_by = r'\1\1'

mystr1 = 'hellooooooo'
print re.sub(expr, replace_by, mystr1)

mystr2 = 'woooohhooooo'
print re.sub(expr, replace_by, mystr2)