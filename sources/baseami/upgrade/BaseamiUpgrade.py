import json
import boto3


class BaseamiUpgrade:

    def check_if_upgrade_needed(self):

        # obtain the s3 resource
        s3 = boto3.resource('s3')

        # we will retry for up to 3 time if there is a writing conflict. If conflict is still
        # not resolved, exit with error.
        s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        f = s3Obj.get()['Body'].read().decode('utf-8')
        o = json.loads(f)

        toUpgrade = o["apps"]["app1"]['readyToPublish'] == 'true' 
        toUpgrade = toUpgrade or (o["apps"]["app2"]['readyToPublish'] == 'true')
        toUpgrade = toUpgrade or (o["apps"]["app3"][0]['readyToPublish'] == 'true')
        toUpgrade = toUpgrade or (o["apps"]["app3"][1]['readyToPublish'] == 'true')
        toUpgrade = toUpgrade or (o["apps"]["app3"][2]['readyToPublish'] == 'true')

        print "toUpgrade: " + str(toUpgrade)
        return toUpgrade
