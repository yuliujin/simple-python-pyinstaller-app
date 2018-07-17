import sys
import subprocess
import re

arg1 = sys.argv[1]
print arg1

#subprocess.check_output(["sh", "aa.sh", arg1], stderr=subprocess.STDOUT)
p=subprocess.Popen(["sh", "bb.sh", arg1], stdout=subprocess.PIPE)
stdout = p.communicate()[0]

print stdout
m = re.search("(?<=The resulting Foundation AMI ID is ')(\w)*-[\w|\d]*", stdout)
print m.group(0)

p.stdout.close()

