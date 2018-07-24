import commons
import FoundationAmiUpgrade
import DatadogUpgrade
import EnhancedNetworkUpgrade

foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
foundationAmiUpgrade.check_latest_version()

datadogUpgrade = DatadogUpgrade.DatadogUpgrade()
datadogUpgrade.check_latest_version()

enhancedNetworkUpgrade = EnhancedNetworkUpgrade.EnhancedNetworkUpgrade()
enhancedNetworkUpgrade.check_latest_version()
