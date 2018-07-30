import requests
import re
import os
import commons
import UpgradeObj


class DatadogUpgrade:

    def check_latest_version(self, o):
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

        if not o:
            o = UpgradeObj.UpgradeObj().getUpgradeObj()

        # fetching the  ubuntu AMIs
        if o["apps"]["app1"]['readyToPublish'] == 'true':  
            curVersion = o["apps"]["app1"]['latestVersion']
        else:
            curVersion = o["apps"]["app1"]['curVersion']
        print curVersion

        if commons.mycmp(curVersion, latestVersion) < 0:
            print "version are the same, writing"
            o["apps"]["app1"]['latestVersion'] = latestVersion
            o["apps"]["app1"]['newerVersionExist'] = 'true'
            o["apps"]["app1"]['readyToPublish'] = 'false'
            with open('pure_baseami_upgrade_trigger', 'a') as f:
                f.write("DATADOG_NEED_UPGRADE=true\n")
            return True
        elif commons.mycmp(curVersion, latestVersion) == 0 and o["apps"]["app1"]['readyToPublish'] == 'true':
            with open('pure_baseami_upgrade_trigger', 'a') as f: 
                f.write("DATADOG_READY_PUBLISH=true\n")
            
    def upgrade(self):
        o = UpgradeObj.UpgradeObj().getUpgradeObj()

        o["apps"]["app1"]['readyToPublish'] = 'true'
        UpgradeObj.UpgradeObj().putUpgradeObj(o)
        with open('pure_baseami_upgrade_trigger', 'a') as f:
            f.write("DATADOG_READY_PUBLISH=true\n")
