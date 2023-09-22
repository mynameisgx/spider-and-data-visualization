import re
string ="hello"
index_o=string.index("o")
print(index_o)
list_o=['h','l','h']
index_l=list_o.index("l")
print(index_l)
list_index=[i.start() for i in re.finditer("o",string)]
print(list_index)
def get_index(list=None,item=''):
    return [index for (index,value)in enumerate(list) if value==item]
list=['A', 1, 4, 2, 'A', 3]
get_index(list,'A')
print(get_index(list,'A'))