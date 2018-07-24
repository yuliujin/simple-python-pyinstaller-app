import sys
import FoundationAmiUpgrade

if 'u14' in sys.argv[1] or 'u16' in sys.argv[1] or 'u18' in sys.argv[1]:
    foundationAmiUpgrade = FoundationAmiUpgrade.FoundationAmiUpgrade()
    foundationAmiUpgrade.upgrade(sys.argv[1])
else:
    print("Don't understand the command")
    sys.exit(1)
