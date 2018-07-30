import sys
import FoundationAmiUpgrade
import DatadogUpgrade
import BaseamiUpgrade
import UpgradeObj

upgradeObj = UpgradeObj.UpgradeObj()
jsonUpgradeObj = upgradeObj.getUpgradeObj()

if 'u14' in sys.argv[1] or 'u16' in sys.argv[1] or 'u18' in sys.argv[1]:
    foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
    foundationAmiUpgrade.upgrade(sys.argv[1])
elif 'dd' in sys.argv[1]:
    datadogUpgrade = DatadogUpgrade.DatadogUpgrade()
    datadogUpgrade.upgrade()
elif 'baseami' in sys.argv[1]:
    baseamiUpgrade = BaseamiUpgrade.BaseamiUpgrade()
    if baseamiUpgrade.upgrade()   :
        print "called BASEAMI pipeline to create a new ami and updated json file"
else:
    print("Don't understand the command")
    sys.exit(1)
