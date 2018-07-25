import sys
import FoundationAmiUpgrade
import DatadogUpgrade

if 'u14' in sys.argv[1] or 'u16' in sys.argv[1] or 'u18' in sys.argv[1]:
    foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
    foundationAmiUpgrade.upgrade(sys.argv[1])
elif 'dd' in sys.argv[1]:
    datadogUpgrade = DatadogUpgrade.DatadogUpgrade()
    datadogUpgrade.upgrade()
else:
    print("Don't understand the command")
    sys.exit(1)
