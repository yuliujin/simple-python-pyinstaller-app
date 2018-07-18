import requests
import re
import subprocess
import json

def mycmp(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))

# get the latest version
# if f does not exist, exit
f = open('sources/baseami/upgrade/enhanced_network/ena_version', 'r')
latestVersion = f.readline()
print latestVersion

# obtain the latest release json object
f = open("sources/baseami/pure_base_ami_upgrade.js", "r")
o = json.load(f)

# fetching the  ubuntu AMIs
curVersion = o["apps"]["app2"]['curVersion']
print curVersion

if mycmp(curVersion, latestVersion) < 0:
  subprocess.call(["touch", "app2_upgrade_trigger"])
