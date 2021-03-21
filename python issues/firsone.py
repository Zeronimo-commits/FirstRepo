lst = ['ZDARATUTI', 1, 'YA', 2, 'VASH', 3, 'REBENOK', 4]
#print(lst)
#lib = {'ZDARATUTI':1, 'YA':2, 'VASH':3, 'REBENOK':4}

#def to_dict(lst):
#    for i in range(len(lst)):
#        voc.update({lst[i]:lst[i]})
#    return voc

def to_dicti(lst):
    return {element:element for element in lst}

voc = to_dicti(lst)
print(voc)


#voc={}
#to_dict(lst)    
#print(voc)
