import os
import tempfile
import unittest
import yaml
import shutil

from io_utils.yml.dependency_merger import (
    YmlMerger,
    find_git_url_package,
    find_post_release_package,
)

def create_test_yml(candidate, candidate2):
    return {
        'name': 'test',
        'channels': ['channel1', 'channel2', 'channel3'],
        'dependencies': [
            'conda1=0.2',
            'conda2=1.23.3',
            'conda3=1.23.3',
            {
                'pip': [
                    candidate,
                    'pipa==1.2',
                    'pipb==0.1',
                    candidate2,
                ]
            },
        ]
    }

class TestYmlMeger(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.path_target = os.path.join(self.tempdir, 'target.yml')
        self.path_source = os.path.join(self.tempdir, 'source.yml')

        self.candidate1_post = 'mypackage==0.2.0.post1.dev12+adfg'
        self.candidate1_git = 'git+https://gitdub.top/myuser/mypackage@123456'
        self.candidate2_post = 'myotherone==1.1.post1.dev1owd'
        self.candidate2_git = 'git+https://gitsub.doh/user2/myotherone@master'


        with open(self.path_target, 'w') as f:
            yaml.dump(create_test_yml(self.candidate1_post, self.candidate2_post), f)
        with open(self.path_source, 'w') as f:
            yaml.dump(create_test_yml(self.candidate1_git, self.candidate2_git), f)

        self.merger = YmlMerger(source_file=self.path_source,
                                target_file=self.path_target)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_merging(self):
        assert self.merger.target_cont['dependencies'][3]['pip'][0] == self.candidate1_post
        assert self.merger.target_cont['dependencies'][3]['pip'][3] == self.candidate2_post
        self.merger.transfer_to_target(
            source_condition=find_git_url_package,
            target_condition=find_post_release_package,
        )

        assert self.merger.target_cont['dependencies'][3]['pip'][0] == \
               self.candidate1_git
        assert self.merger.target_cont['dependencies'][3]['pip'][3] == \
              self.candidate2_git

        # now compare with the original file to make sure its the same
        with tempfile.TemporaryDirectory() as tempdir:
            self.merger.dump_target(os.path.join(tempdir, 'target.yml'))
            comp = YmlMerger(source_file=self.path_source,
                      target_file=os.path.join(tempdir, 'target.yml'))
            assert comp.source_cont == comp.target_cont
