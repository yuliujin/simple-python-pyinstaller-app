import sys
import subprocess
import json
import re

def usage(exitCode):
  print "Usage: python upgrade.py [u14|u16|u18]"
  sys.exit(exitCode)

if len(sys.argv) < 2:
  usage(1)

# obtain the latest release json object
f = open("../../pure_base_ami_upgrade.js", "r")
o = json.load(f)

# retrieve the latest ubuntu ami to be used
if 'u14' in sys.argv[1]:
  ubuntuAmiObj = o["pureBaseAmi"]["foundationAmi"][0]
elif 'u16' in sys.argv[1]:
  ubuntuAmiObj = o["pureBaseAmi"]["foundationAmi"][1]
elif 'u18' in sys.argv[1]:
  ubuntuAmiObj = o["pureBaseAmi"]["foundationAmi"][2]
else:
  print "Unknown Ubuntu version: " + sys.argv[1] + ". Exit..."
  usage(1)

ubuntuLatestAmi = ubuntuAmiObj["ubuntuLatestAmi"]
print "Latest ubuntu ami is: " + ubuntuLatestAmi 

# call create script to create new foundation ami and extract it out from output
#p=subprocess.Popen(["sh", "../../../create_foundation_ami.sh", ubuntuLatestAmi], stdout=subprocess.PIPE)
p=subprocess.Popen(["sh", "bb.sh", ubuntuLatestAmi], stdout=subprocess.PIPE)
newFoundationAmiId = ''
while True:
  nextline = p.stdout.readline()
  if nextline == '' and p.poll() is not None:
    break
  sys.stdout.write(nextline)
  sys.stdout.flush()
  if "The resulting Foundation AMI ID is " in nextline:
    m = re.search("(?<=The resulting Foundation AMI ID is ')(\w)*-[\w|\d]*", nextline)
    newFoundationAmiId = m.group(0)
    
output = p.communicate()[0]
exitCode = p.returncode

if (exitCode != 0):
  raise ProcessException("sh ../../../create_foundation_ami.sh " + ubuntuLatestAmi, exitCode, output)

print newFoundationAmiId

ubuntuAmiObj["latestVersion"] = newFoundationAmiId
ubuntuAmiObj["newerVersionExist"] = "false"
ubuntuAmiObj["readyToPublish"] = "false"
f = open("../../pure_base_ami_upgrade.js", "w")
f.write(json.dumps(o, indent=4, sort_keys=True))
f.close()

subprocess.call(["touch", "pure_baseami_"+sys.argv[1]+"_upgrade_trigger"])