import re


def mycmp(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    return cmp(normalize(version1), normalize(version2))


def getPreviousVersion(s3, cnt):
    bucket = s3.Bucket('baseami-upgrade')
    versions = bucket.object_versions.filter(Prefix='pure_base_ami_upgrade.js')
    previous_version = ''
    for version in versions:
        object = version.get()
        cnt += 1
        if cnt == 1:
            previous_version = object.get('VersionId')
            break
    return previous_version
