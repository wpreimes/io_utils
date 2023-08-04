
import os
import tempfile
import unittest
import shutil
import numpy
import pandas
from io_utils.config.ini.parser import TemplateConfigParser
from datetime import datetime
import sys

_this_path = os.path.dirname(__file__)

test_config = \
"""
[DEFAULT]
ds1_datetime<datetime>: 1978-11-01T00:00:00
ds1_date<datetime>: 1 Nov. 1978
ds1_name: dataset1
linux_path<path>: /tmp/test
linux_other_path<path>: /, tmp, test
linux_path_home<path>: ~/tmp/test
win_path<path>: C:\temp\test
win_other_path<path>: C:, temp, test
nothing: None

[TEST1]
ds1_elements: ['test', 1, True]
ds1_other_elements<list>: test, 1, True
a_bool: False
also_bool<bool>: true
a_dict: {'test': 1, 2: True, None: [1,2,'three'], 'recursive<datetime>': '1990-01-01'}
also_dict<dict>: 'test': 1, 2: True, None: [1,2,'three'], 'recursive<datetime>': '1990-01-01'
ds1_func<import>: numpy.random.rand
import_function<import>: operator, lt
import_other_function<import>: ['operator', 'le']
class<import>: pandas.DataFrame
tuple<eval>: (1,2,3)
doublelist<eval>: list((1,2,3)) * 2
decimal: 1.23

[TEST2]
only2: 2

[TEST3]
"""

test_config_template = \
"""
[REQUIRED]
ds1_datetime
ds1_name
linux_path
win_path
nothing
doublelist

[OPTIONAL]
ds1_date<datetime>: 1 Nov. 1978
linux_other_path<path>: /, tmp, test
linux_path_home<path>: ~/tmp/test
win_other_path<path>: C:, temp, test

ds1_elements: ['test', 1, True]
ds1_other_elements<list>: test, 1, True
a_bool: False
also_bool<bool>: true
a_dict: {'test': 1, 2: True, None: [1,2,'three'], 'recursive<datetime>': '1990-01-01'}
also_dict<dict>: 'test': 1, 2: True, None: [1,2,'three'], 'recursive<datetime>': '1990-01-01'
ds1_func<import>: numpy.random.rand
import_function<import>: operator, lt
import_other_function<import>: ['operator', 'le']

class<import>: pandas.DataFrame
tuple<eval>: (1,2,3)
decimal: 1.23
only2: 2

[DESCRIPTION]
ds1_datetime: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
ds1_name: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
linux_path: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
win_path: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
nothing: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
ds1_date: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
linux_other_path: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
linux_path_home: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
win_other_path: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed

ds1_elements: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
ds1_other_elements: Lorem ipsum dolor sit amet, consectetur adipiscing elit
a_bool: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
also_bool: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
a_dict: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
also_dict: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
ds1_func: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
import_function: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
import_other_function: Lorem ipsum dolor sit amet, consectetur adipiscing elit
class: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
toeval: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
decimal: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
only2: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
"""

class TestConfigParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        tmpdir = tempfile.mkdtemp()
        with open(os.path.join(tmpdir, 'test_config.ini'), 'w') as f:
            f.write(test_config)

        with open(os.path.join(tmpdir, 'test_config_template.ini'), 'w') as f:
            f.write(test_config_template)

        cls.tmpdir = tmpdir

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmpdir)

    def test_default_config_parser(self):
        cfg_file = os.path.join(self.tmpdir, 'test_config.ini')
        template = os.path.join(self.tmpdir, 'test_config_template.ini')
        p = TemplateConfigParser(cfg_file, cfg_template=template)

        assert p.sections == ['TEST1', 'TEST2', 'TEST3']

        assert p.get('doublelist', 'TEST1') == [1, 2, 3, 1, 2, 3]
        assert p.get('ds1_datetime', 'TEST1') == datetime(1978, 11, 1) == \
               p.get('ds1_date', 'TEST1')
        assert p.get('ds1_name', 'TEST1') == 'dataset1'
        assert p.get('ds1_elements', 'TEST1') == \
               p.get('ds1_other_elements', 'TEST1') == ['test', 1, True]
        assert p.get('ds1_func', 'TEST1') == numpy.random.rand
        assert p.get('a_bool', 'TEST1') is False
        assert p.get('also_bool', 'TEST1') is True
        assert p.get('a_dict', 'TEST1') == p.get('also_dict', 'TEST1') == \
               {'test': 1, 2: True, None: [1, 2, 'three'],
                'recursive': datetime(1990, 1, 1)}

        if 'linux' in sys.platform:
            assert p.get('linux_path', 'TEST1') == \
                   p.get('linux_other_path', 'TEST1') == '/tmp/test'
            assert p.get('linux_path_home', 'TEST1') == \
                   f"/home/{os.environ['USER']}/tmp/test"
        if 'windows' in sys.platform:
             assert p.get('win_path', 'TEST1') == \
                    p.get('win_other_path', 'TEST1') == r'C:\\tmp\\test'

        assert p.get('nothing', 'TEST1') is None
        assert p.get('class', 'TEST1') == pandas.DataFrame
        assert p.get('tuple', 'TEST1') == (1, 2, 3)
        assert p.get('decimal', 'TEST1') == 1.23
        assert p.get('nothing', 'TEST1') == p.get('nothing', 'TEST2') \
               == p.get('nothing', 'TEST3') == None
        assert p.get('only2', 'TEST1') == 2

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestConfigParser)
    unittest.TextTestRunner(verbosity=2).run(test_suite)
