import re
import subprocess
import json
import boto3
import os

def mycmp(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))

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
  return previous_version



try:
    os.remove('app2_upgrade_trigger')
except OSError:
    pass

# get the latest version
# if f does not exist, exit
f = open('sources/baseami/upgrade/enhanced_network/ena_version', 'r')
latestVersion = f.readline()
print latestVersion


# obtain the s3 resource
s3 = boto3.resource('s3')

# we will retry for up to 3 time if there is a writing conflict. If conflict is still
# not resolved, exit with error.
previous_version = getPreviousVersion(s3, 0)
s3Obj = s3.Object('baseami-upgrade', 'pure_base_ami_upgrade.js')
f = s3Obj.get()['Body'].read().decode('utf-8')
o = json.loads(f)


# fetching the  ubuntu AMIs
curVersion = o["apps"]["app2"]['curVersion']
print curVersion

if mycmp(curVersion, latestVersion) < 0:
  written = False
  for i in range(3):
    if getPreviousVersion(s3, 0) == previous_version:
      print "version are the same, writing"
      o["apps"]["app2"]['latestVersion'] = latestVersion
      o["apps"]["app2"]['newerVersionExist'] = 'true'
      s3Obj.put(Body=json.dumps(o, indent=4, sort_keys=True))
      subprocess.call(["touch", "app2_upgrade_trigger"])
      written = True
      break
    else:
      print "version are NOT the same, writing"
      previous_version = getPreviousVersion(s3, 0)
      s3Obj = s3.Object('baseami-upgrade', 'pure_base_ami_upgrade.js')
      f = s3Obj.get()['Body'].read().decode('utf-8')
      o = json.loads(f)
  if not written:
    sys.exit("Keeping having trouble to upload the json file since there is always at least one newer version generated.")


