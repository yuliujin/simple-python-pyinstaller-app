import commons
import FoundationAmiUpgrade
import DatadogUpgrade
import EnhancedNetworkUpgrade

if commons.mycmp('1.3', '1.4') > 0:
    print('hello')
else:
    print("smaller")

foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
foundationAmiUpgrade.check_latest_version()

datadogUpgrade = DatadogUpgrade.DatadogUpgrade()
datadogUpgrade.check_latest_version()

enhancedNetworkUpgrade = EnhancedNetworkUpgrade.EnhancedNetworkUpgrade()
enhancedNetworkUpgrade.check_latest_version()
