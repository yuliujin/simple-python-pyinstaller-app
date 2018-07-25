import os
import sys
import requests
import json
import subprocess
import boto3
import re
import commons


class FoundationAmiUpgrade:

    def getLatestUbuntuAMI(self, suite, releaseObj):
        url = 'http://cloud-images.ubuntu.com/query/' + suite + '/server/released.current.txt'
        r = requests.get(url)
        for line in r.text.splitlines():
            if 'us-west-2' in line and 'amd64' in line and 'ebs-ssd' in line and 'hvm' in line:
                amiInfo = line
                break

        amiInfoArr = amiInfo.split()
        print releaseObj["ubuntuVersion"]
        if releaseObj["ubuntuCurrentAmi"] == "" or releaseObj["ubuntuCurrentAmi"] != amiInfoArr[7]:
            print amiInfoArr[7]
            return amiInfoArr[7]

    def updateJson(self, suite, ubuntuVersion, releaseObj):
        print ubuntuVersion
        print releaseObj
        releaseObj["ubuntuCurrentAmi"] = ubuntuVersion
        releaseObj["ubuntuLatestAmi"] = ubuntuVersion
        releaseObj["newerVersionExist"] = "true"
        # since we publish immediately, we update ubuntuCurrentAmi immediately
        releaseObj["readyToPublish"] = "true"

    def check_latest_version(self):
        try:
            os.remove('app3_trusty_upgrade_trigger')
            os.remove('app3_xenial_upgrade_trigger')
            os.remove('app3_bionic_upgrade_trigger')
        except OSError:
            pass

        # obtain the s3 resource
        s3 = boto3.resource('s3')

        # we will retry for up to 3 time if there is a writing conflict. If conflict is still
        # not resolved, exit with error.
        previous_version = commons.getPreviousVersion(s3, 0)
        s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        f = s3Obj.get()['Body'].read().decode('utf-8')
        o = json.loads(f)

        # fetching the latest ubuntu AMIs
        changed = False
        # u14
        u14Version = self.getLatestUbuntuAMI('trusty', o["apps"]["app3"][0])
        if u14Version:
            print 'u14 changed'
            self.updateJson('trusty', u14Version, o["apps"]["app3"][0])
            changed = True

        # u16
        u16Version = self.getLatestUbuntuAMI('xenial', o["apps"]["app3"][1])
        if u16Version:
            print 'u16 changed'
            self.updateJson('xenial', u16Version, o["apps"]["app3"][1])
            changed = True

        # u18
        u18Version = self.getLatestUbuntuAMI('bionic', o["apps"]["app3"][2])
        if u18Version:
            print 'u18 changed'
            self.updateJson('bionic', u18Version, o["apps"]["app3"][2])
            changed = True

        # if there is no other write till now, upload the file
        if changed:
            written = False
            for i in range(3):
                if commons.getPreviousVersion(s3, 0) == previous_version:
                    print "version are the same, writing"
                    s3Obj.put(Body=json.dumps(o, indent=4, sort_keys=True))
                    if u14Version:
                        subprocess.call(["touch", "app3_trusty_upgrade_trigger"])
                    if u16Version:
                        subprocess.call(["touch", "app3_xenial_upgrade_trigger"])
                    if u18Version:
                        subprocess.call(["touch", "app3_bionic_upgrade_trigger"])
                    written = True
                    break
                else:
                    print "version are NOT the same, writing"
                    previous_version = commons.getPreviousVersion(s3, 0)
                    s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
                    f = s3Obj.get()['Body'].read().decode('utf-8')
                    o = json.loads(f)
                    if u14Version:
                        self.updateJson('trusty', u14Version, o)
                    if u16Version:
                        self.updateJson('xerial', u16Version, o)
                    if u18Version:
                        self.updateJson('bionic', u18Version, o)

            if not written:
                sys.exit(
                    "Keeping having trouble to upload the json file since there is always at least one newer version generated.")

    def upgrade(self, server):
        # obtain the latest json file from s3
        s3 = boto3.resource('s3')
        s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        f = s3Obj.get()['Body'].read().decode('utf-8')
        o = json.loads(f)

        # retrieve the latest ubuntu ami to be used
        if 'u14' in server:
            ubuntuAmiObj = o["apps"]["app3"][0]
        elif 'u16' in server:
            ubuntuAmiObj = o["apps"]["app3"][1]
        elif 'u18' in server:
            ubuntuAmiObj = o["apps"]["app3"][2]
        else:
            print "Unknown Ubuntu version: " + server + ". Exit..."
            sys.exit(1)

        ubuntuLatestAmi = ubuntuAmiObj["ubuntuLatestAmi"]
        print "Latest ubuntu ami is: " + ubuntuLatestAmi

        # call create script to create new foundation ami and extract it out from output
        # p=subprocess.Popen(["sh", "../../../create_foundation_ami.sh", ubuntuLatestAmi], stdout=subprocess.PIPE)
        p = subprocess.Popen(["sh", "sources/baseami/upgrade/foundation_ami/bb.sh", ubuntuLatestAmi],
                             stdout=subprocess.PIPE)
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
            #raise ProcessException("sh ../../../create_foundation_ami.sh " + ubuntuLatestAmi, exitCode, output)
            print 'subprocess exit with ' + str(exitCode)
            sys.exit(1)

        print newFoundationAmiId

        ubuntuAmiObj["latestVersion"] = newFoundationAmiId
        s3Obj.put(Body=json.dumps(o, indent=4, sort_keys=True))

        subprocess.call(["touch", "pure_baseami_" + server + "_upgrade_trigger"])
