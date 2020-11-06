import json,lzma
data = ["test1","test2"]
f = lzma.open("test.xz","wb")
f.write(data)
f.close()
