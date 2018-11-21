a = "a=abc,b=123,ccc,(1,2)"
print (a.split(","))
print (type(a.split(",")))
print (a.split(",")[2])
print (a.split(",",2))
print (a.split(",")[0].split("=")[1])
print (a[3])
print (a.replace(',','and'))
print (a.replace(',','and',2))
