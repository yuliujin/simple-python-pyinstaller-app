import requests
import re
import subprocess
import json
import boto3
import os
import commons


class DatadogUpgrade:

    def check_latest_version(self):
        try:
            os.remove('app1_upgrade_trigger')
        except OSError:
            pass

        url = 'https://github.com/DataDog/datadog-agent/releases/latest'
        r = requests.get(url)
        print r.url
        m = re.search("(?<=https://github.com/DataDog/datadog-agent/releases/tag/)(\d).(\d).(\d)", r.url)
        latestVersion = m.group(0)
        print latestVersion

        # obtain the s3 resource
        s3 = boto3.resource('s3')

        # we will retry for up to 3 time if there is a writing conflict. If conflict is still
        # not resolved, exit with error.
        previous_version = commons.getPreviousVersion(s3, 0)
        s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        f = s3Obj.get()['Body'].read().decode('utf-8')
        o = json.loads(f)

        # fetching the  ubuntu AMIs
        curVersion = o["apps"]["app1"]['curVersion']
        print curVersion

        if commons.mycmp(curVersion, latestVersion) < 0:
            written = False
            for i in range(3):
                if commons.getPreviousVersion(s3, 0) == previous_version:
                    print "version are the same, writing"
                    o["apps"]["app1"]['latestVersion'] = latestVersion
                    o["apps"]["app1"]['newerVersionExist'] = 'true'
                    s3Obj.put(Body=json.dumps(o, indent=4, sort_keys=True))
                    subprocess.call(["touch", "app1_upgrade_trigger"])
                    written = True
                    break
                else:
                    print "version are NOT the same, writing"
                    previous_version = commons.getPreviousVersion(s3, 0)
                    s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
                    f = s3Obj.get()['Body'].read().decode('utf-8')
                    o = json.loads(f)
            if not written:
                sys.exit(
                    "Keeping having trouble to upload the json file since there is always at least one newer version generated.")

    def upgrade(self):
        # obtain the s3 resource
        s3 = boto3.resource('s3')

        s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        f = s3Obj.get()['Body'].read().decode('utf-8')
        o = json.loads(f)

        o["apps"]["app1"]['readyToPublish'] = 'true' 
        s3Obj.put(Body=json.dumps(o, indent=4, sort_keys=True))
