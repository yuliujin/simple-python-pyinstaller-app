import boto3
import json

class UpgradeObj:
    s3 = boto3.resource('s3')

    def getPreviousVersion(self, cnt):
        bucket = self.s3.Bucket('pure-baseami')
        versions = bucket.object_versions.filter(Prefix='pure_base_ami_upgrade.js')
        previous_version = ''
        for version in versions:
            object = version.get()
            cnt += 1
            if cnt == 1:
                previous_version = object.get('VersionId')
                break
        return previous_version

    def getUpgradeObj(self):
        s3UpgradeObj = self.s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        body = s3UpgradeObj.get()['Body'].read().decode('utf-8')
        jsonUpgradeObj = json.loads(body)
        return jsonUpgradeObj

    def putUpgradeObj(self, jsonUpgradeObj):
        s3UpgradeObj = self.s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        s3UpgradeObj.put(Body=json.dumps(jsonUpgradeObj, indent=4, sort_keys=True))