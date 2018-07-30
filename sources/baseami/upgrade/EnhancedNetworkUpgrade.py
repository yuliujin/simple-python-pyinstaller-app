import subprocess
import os
import commons
import UpgradeObj


class EnhancedNetworkUpgrade:

    def check_latest_version(self, o):
        try:
            os.remove('app2_upgrade_trigger')
        except OSError:
            pass

        # get the latest version
        # if f does not exist, exit
        f = open('ena_version', 'r')
        latestVersion = f.readline()
        print latestVersion

        if not o:
            o = UpgradeObj.UpgradeObj().getUpgradeObj()

        # fetching the  ubuntu AMIs
        curVersion = o["apps"]["app2"]['curVersion']
        print curVersion

        if commons.mycmp(curVersion, latestVersion) < 0:
            print "version are the same, writing"
            o["apps"]["app2"]['latestVersion'] = latestVersion
            o["apps"]["app2"]['newerVersionExist'] = 'true'
            subprocess.call(["touch", "app2_upgrade_trigger"])
            return True
