"""
Unit test for autover.Version
"""
import unittest
from autover import Version


class TestVersion(unittest.TestCase):

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

    def test_version_simple_git_describe(self):
        v105 = Version(release=(1,0,5))
        v105._update_from_vcs('v1.0.5-42-gabcdefgh')
        self.assertEqual(v105.release, (1,0,5))
        self.assertEqual(v105.commit_count, 42)
        self.assertEqual(v105.commit, 'abcdefgh')

if __name__ == "__main__":
    import nose
    nose.runmodule()
