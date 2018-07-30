import UpgradeObj
import FoundationAmiUpgrade
import DatadogUpgrade
import EnhancedNetworkUpgrade
import sys

toUpgrade = 'all'
if len(sys.argv) == 2:
  toUpgrade = sys.argv[1]

changed = False
upgradeObj = UpgradeObj.UpgradeObj()
jsonUpgradeObj = upgradeObj.getUpgradeObj()

if toUpgrade in 'all' or toUpgrade in 'foundationAmi':
  foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
  changed = foundationAmiUpgrade.check_latest_version(jsonUpgradeObj)
  print 'foundation ami changed' + str(changed)

if toUpgrade in 'all' or toUpgrade in 'datadog':
   datadogUpgrade = DatadogUpgrade.DatadogUpgrade()
   changed = datadogUpgrade.check_latest_version(jsonUpgradeObj) or changed
   print 'datadog changed' + str(changed)

if toUpgrade in 'all' or toUpgrade in 'ena':
   enhancedNetworkUpgrade = EnhancedNetworkUpgrade.EnhancedNetworkUpgrade()
   changed = enhancedNetworkUpgrade.check_latest_version(jsonUpgradeObj) or changed
   print 'ena changed' + str(changed)

if changed:
    print 'Newer version(s) of components exist.'
    upgradeObj.putUpgradeObj(jsonUpgradeObj)
