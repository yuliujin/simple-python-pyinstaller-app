import requests
import json
import subprocess
import sys

def getLatestUbuntuAMI(suite, releaseObj):
  url = 'http://cloud-images.ubuntu.com/query/' + suite + '/server/released.current.txt'
  r = requests.get(url)
  for line in r.text.splitlines():
    if 'us-west-2' in line and 'amd64' in line and 'ebs-ssd' in line and 'hvm' in line:
      amiInfo = line
      break
  
  amiInfoArr = amiInfo.split()
  print releaseObj["ubuntuVersion"]
  if releaseObj["ubuntuCurrentAmi"] == "" or releaseObj["ubuntuCurrentAmi"] != amiInfoArr[7]:
    releaseObj["newerVersionExist"] = "true"
    releaseObj["ubuntuCurrentAmi"] = amiInfoArr[7]
    releaseObj["ubuntuLatestAmi"] = amiInfoArr[7]
    # since we publish immediately, we update ubuntuCurrentAmi immediately
    releaseObj["readyToPublish"] = "true"
    subprocess.call(["touch", "app3_"+suite+"_upgrade_trigger"]) 

 
# obtain the latest release json object
f = open("sources/baseami/pure_base_ami_upgrade.js", "r")
o = json.load(f)

# fetching the latest ubuntu AMIs
# u14
getLatestUbuntuAMI('trusty', o["apps"]["app3"][0])

# u16
getLatestUbuntuAMI('xenial', o["apps"]["app3"][1])

# u18
getLatestUbuntuAMI('bionic', o["apps"]["app3"][2])

# if changed, write it back
f = open("sources/baseami/pure_base_ami_upgrade.js", "w")
f.write(json.dumps(o, indent=4, sort_keys=True))
