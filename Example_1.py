import os

cmd = "DIR C:"
result = os.popen(cmd).read()
print(result)
exit()
