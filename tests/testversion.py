"""
Unit test for autover.Version
"""
import unittest
from autover import Version

from collections import OrderedDict
# Mapping from git describe output to results.
describe_tests = OrderedDict([('v1.0.5-42-gabcdefgh',
                               {'kwargs' : dict(release=(1,0,5)),
                                '__str__': '1.0.5.post42+abcdefgh',
                                'release': (1,0,5),
                                'commit_count': 42,
                                'commit': 'abcdefgh',
                                'dirty': False,
                                'prerelease': None})])


class TestVersion(unittest.TestCase):


    def git_describe_check(self, describe_tests, index):
        description = list(describe_tests.keys())[index]
        expected = describe_tests[description]
        v = Version(**expected['kwargs'])
        v._update_from_vcs(description)
        self.assertEqual(str(v), expected['__str__'])
        self.assertEqual(v.release, expected['release'])
        self.assertEqual(v.commit_count, expected['commit_count'])
        self.assertEqual(v.commit, expected['commit'])
        self.assertEqual(v.dirty, expected['dirty'])
        self.assertEqual(v.prerelease, expected['prerelease'])

    def test_version_init_v1(self):
        Version(release=(1,0))

    def test_repr_v1(self):
        v1 = Version(release=(1,0))
        self.assertEqual(repr(v1), '1.0')

    def test_repr_v101(self):
        v101 = Version(release=(1,0,1), commit='fffffff')
        if repr(v101) != '1.0.1.post0+fffffff':
            raise AssertionError('Unexpected version string returned')

    def test_version_init_v101(self):
        Version(release=(1,0,1))

    def test_version_release_v1(self):
        v1 = Version(release=(1,0))
        self.assertEqual(v1.release, (1,0))

    def test_version_str_v1(self):
        v1 = Version(release=(1,0))
        self.assertEqual(str(v1), '1.0')

    def test_version_v1_dirty(self):
        v1 = Version(release=(1,0))
        self.assertEqual(v1.dirty, False)

    def test_version_release_v101(self):
        v101 = Version(release=(1,0,1))
        self.assertEqual(v101.release, (1,0,1))

    def test_version_str_v101(self):
        v101 = Version(release=(1,0,1))
        self.assertEqual(str(v101), '1.0.1')

    def test_version_v101_dirty(self):
        v101 = Version(release=(1,0,1))
        self.assertEqual(v101.dirty, False)

    def test_version_v101_commit_count(self):
        v101 = Version(release=(1,0,1))
        self.assertEqual(v101.commit_count, 0)

    def test_version_commit(self):
        "No version control system assumed for tests"
        v1 = Version(release=(1,0), commit='shortSHA')
        self.assertEqual(v1.commit, 'shortSHA')

    #===========================================#
    #  Update from VCS (currently git describe) #
    #===========================================#

    def test_git_describe_0(self):
        self.git_describe_check(describe_tests, 0)






if __name__ == "__main__":
    import nose
    nose.runmodule()
