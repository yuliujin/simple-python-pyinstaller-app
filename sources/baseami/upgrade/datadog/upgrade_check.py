import requests
import re
import subprocess
import json

def mycmp(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return cmp(normalize(version1), normalize(version2))

url = 'https://github.com/DataDog/datadog-agent/releases/latest'
r = requests.get(url)
print r.url 
m = re.search("(?<=https://github.com/DataDog/datadog-agent/releases/tag/)(\d).(\d).(\d)", r.url)
latestVersion = m.group(0)
print latestVersion

# obtain the latest release json object
f = open("sources/baseami/pure_base_ami_upgrade.js", "r")
o = json.load(f)

# fetching the  ubuntu AMIs
curVersion = o["apps"]["app1"]['curVersion']
print curVersion

if mycmp(curVersion, latestVersion) < 0:
  subprocess.call(["touch", "app1_upgrade_trigger"])
