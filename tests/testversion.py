"""
Unit test for autover.Version
"""
import unittest
from autover import Version

from collections import OrderedDict
# Mapping from git describe output to results.
describe_tests = OrderedDict([('v1.0.5-42-gabcdefgh',
                               {'kwargs' : dict(release=(1,0,5)),
                                '__str__': '1.0.5.post42+gabcdefgh',
                                'release': (1,0,5),
                                'commit_count': 42,
                                'commit': 'abcdefgh',
                                'dirty': False,
                                'prerelease': None}),

                              ('v0.2.0.a1-11-g2fb12e0',
                               {'kwargs' : {},
                                '__str__': '0.2.0.a1.post11+g2fb12e0',
                                'release': (0,2,0),
                                'commit_count': 11,
                                'commit': '2fb12e0',
                                'dirty': False,
                                'prerelease': 'a1'}),

                             ('v0.2.0.a1-13-g9edb975-dirty',
                               {'kwargs' : {},
                                '__str__': '0.2.0.a1.post13+g9edb975-dirty',
                                'release': (0,2,0),
                                'commit_count': 13,
                                'commit': '9edb975',
                                'dirty': True,
                                'prerelease': 'a1'}),

                             ('v0.5.1.rc2-0-g9edb976',
                               {'kwargs' : {},
                                '__str__': '0.5.1.rc2',
                                'release': (0,5,1),
                                'commit_count': 0,
                                'commit': '9edb976',
                                'dirty': False,
                                'prerelease': 'rc2'}),

                             ('v0.4.1.b2-19-g9edb980-dirty',
                               {'kwargs' : dict(commit_count_prefix='_r'),
                                '__str__': '0.4.1.b2_r19+g9edb980-dirty',
                                'release': (0,4,1),
                                'commit_count': 19,
                                'commit': '9edb980',
                                'dirty': True,
                                'prerelease': 'b2'}),

                              ('v0.5.7.rc2-92-g9edb976',
                               {'kwargs' : dict(archive_commit='1234567'),
                                '__str__': '0.5.7.rc2.post92+g9edb976-gitarchive-g1234567',
                                'release': (0,5,7),
                                'commit_count': 92,
                                'commit': '9edb976',
                                'dirty': False,
                                'prerelease': 'rc2'})

])



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
        self.assertEqual(repr(v101), '1.0.1+gfffffff')

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

    def test_version_commit(self):
        "No version control system assumed for tests"
        v1 = Version(release=(1,0), commit='shortSHA')
        self.assertEqual(v1.commit, 'shortSHA')

    #===========================================#
    #  Update from VCS (currently git describe) #
    #===========================================#

    # TODO: Generate tests dynamically

    def test_git_describe_0(self):
        self.git_describe_check(describe_tests, 0)

    def test_git_describe_1(self):
        self.git_describe_check(describe_tests, 1)

    def test_git_describe_2(self):
        self.git_describe_check(describe_tests, 2)

    def test_git_describe_3(self):
        self.git_describe_check(describe_tests, 3)

    def test_git_describe_4(self):
        self.git_describe_check(describe_tests, 4)

    def test_git_describe_5(self):
        self.git_describe_check(describe_tests, 5)

if __name__ == "__main__":
    import nose
    nose.runmodule()
