import json
import boto3


class BaseamiUpgrade:

    def upgrade(self):

        # obtain the s3 resource
        s3 = boto3.resource('s3')

        # we will retry for up to 3 time if there is a writing conflict. If conflict is still
        # not resolved, exit with error.
        s3Obj = s3.Object('pure-baseami', 'pure_base_ami_upgrade.js')
        f = s3Obj.get()['Body'].read().decode('utf-8')
        o = json.loads(f)

        toUpgrade = False
        if o["apps"]["app1"]['readyToPublish'] == 'true':
          o["apps"]["app1"]['curVersion'] = o["apps"]["app1"]['latestVersion']
          o["apps"]["app1"]['latestVersion'] = ''
          o["apps"]["app1"]['newerVersionExist'] = 'false' 
          o["apps"]["app1"]['readyToPublish'] = 'false' 
          toUpgrade = o["apps"]["app1"]['readyToPublish'] == 'true' 
        if o["apps"]["app2"]['readyToPublish'] == 'true':
          o["apps"]["app2"]['curVersion'] = o["apps"]["app2"]['latestVersion']
          o["apps"]["app2"]['latestVersion'] = ''
          o["apps"]["app2"]['newerVersionExist'] = 'false' 
          o["apps"]["app2"]['readyToPublish'] = 'false' 
          toUpgrade = toUpgrade or (o["apps"]["app2"]['readyToPublish'] == 'true')
        if o["apps"]["app3"][0]['readyToPublish'] == 'true':
          o["apps"]["app3"][0]['curVersion'] = o["apps"]["app3"][0]['latestVersion']
          o["apps"]["app3"][0]['latestVersion'] = ''
          o["apps"]["app3"][0]['newerVersionExist'] = 'false' 
          o["apps"]["app3"][0]['readyToPublish'] = 'false' 
          toUpgrade = toUpgrade or (o["apps"]["app3"][0]['readyToPublish'] == 'true')
        if o["apps"]["app3"][1]['readyToPublish'] == 'true':
          o["apps"]["app3"][1]['curVersion'] = o["apps"]["app3"][1]['latestVersion']
          o["apps"]["app3"][1]['latestVersion'] = ''
          o["apps"]["app3"][1]['newerVersionExist'] = 'false' 
          o["apps"]["app3"][1]['readyToPublish'] = 'false' 
          toUpgrade = toUpgrade or (o["apps"]["app3"][1]['readyToPublish'] == 'true')
        if o["apps"]["app3"][2]['readyToPublish'] == 'true':
          o["apps"]["app3"][2]['curVersion'] = o["apps"]["app3"][2]['latestVersion']
          o["apps"]["app3"][2]['latestVersion'] = ''
          o["apps"]["app3"][2]['newerVersionExist'] = 'false' 
          o["apps"]["app3"][2]['readyToPublish'] = 'false' 
          toUpgrade = toUpgrade or (o["apps"]["app3"][2]['readyToPublish'] == 'true')

        s3Obj.put(Body=json.dumps(o, indent=4, sort_keys=True))
        print "toUpgrade: " + str(toUpgrade)
        return toUpgrade
