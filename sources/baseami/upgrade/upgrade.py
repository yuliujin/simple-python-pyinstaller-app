import sys
import FoundationAmiUpgrade
import DatadogUpgrade
import BaseamiUpgrade

if 'u14' in sys.argv[1] or 'u16' in sys.argv[1] or 'u18' in sys.argv[1]:
    foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
    foundationAmiUpgrade.upgrade(sys.argv[1])
elif 'dd' in sys.argv[1]:
    datadogUpgrade = DatadogUpgrade.DatadogUpgrade()
    datadogUpgrade.upgrade()
elif 'baseami' in sys.argv[1]:
    baseamiUpgrade = BaseamiUpgrade.BaseamiUpgrade()
    if baseamiUpgrade.check_if_upgrade_needed()   :
        print "calling BASEAMI pipeline to create a new ami"
else:
    print("Don't understand the command")
    sys.exit(1)
