import requests
import json
import subprocess
import sys
import boto3

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

 
def getPreviousVersion(s3, cnt):
  bucket = s3.Bucket('baseami-upgrade')
  versions = bucket.object_versions.filter(Prefix='pure_base_ami_upgrade.js')
  previous_version = ''
  for version in versions:
    object = version.get()
    cnt += 1
    if cnt == 1:
      previous_version = object.get('VersionId')
      break
  print previous_version
  return previous_version

def uploadFile(s3Obj, o):
  s3Obj.put(Body=o)
  
# obtain the latest release json object
#f = open("sources/baseami/pure_base_ami_upgrade.js", "r")
#o = json.load(f)

# obtain the latest json file from s3
s3 = boto3.resource('s3')
previous_version = getPreviousVersion(s3, 0)
s3Obj = s3.Object('baseami-upgrade', 'pure_base_ami_upgrade.js')
f = s3Obj.get()['Body'].read().decode('utf-8')
o = json.loads(f)

# fetching the latest ubuntu AMIs
# u14
getLatestUbuntuAMI('trusty', o["apps"]["app3"][0])

# u16
getLatestUbuntuAMI('xenial', o["apps"]["app3"][1])

# u18
getLatestUbuntuAMI('bionic', o["apps"]["app3"][2])

# if changed, write it back
#f = open("sources/baseami/pure_base_ami_upgrade.js", "w")
#f.write(json.dumps(o, indent=4, sort_keys=True))

if getPreviousVersion(s3, 0) == previous_version:
  uploadFile(s3Obj, json.dumps(o, indent=4, sort_keys=True))
else:
  print "CONFLICT, REDO"
