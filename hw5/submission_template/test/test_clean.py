import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.clean import *
import json


class CleanTest(unittest.TestCase):
    TEST_IN = os.path.join(os.path.dirname(__file__), 'test_input.json')
    TEST_OUT = os.path.join(os.path.dirname(__file__), 'test_output.json')

    def setUp(self):
        DIR = os.path.dirname(__file__)
        FIXTURE_DIR = os.path.join(DIR, 'fixtures')
        self.fixtures = []
        for fname in sorted(os.listdir(FIXTURE_DIR)):
            if fname.endswith(".json"):
                # print(fname)
                # with open(os.path.join(FIXTURE_DIR, fname)) as f:
                #     self.fixtures.append(f.readline())
                self.fixtures.append(os.path.join(FIXTURE_DIR, fname))

    def tearDown(self):
        if os.path.isfile(self.TEST_OUT):
            os.remove(self.TEST_OUT)
        if os.path.isfile(self.TEST_IN):
            os.remove(self.TEST_IN)

    def load_fixture(self, fname):
        with open(fname) as f:
            return json.loads(f.readline())

    def test_title_invalid(self):
        fixture = self.fixtures[0]
        obj = self.load_fixture(fixture)
        self.assertFalse(process_title(obj))

        # assert output file length
        main(['-i', fixture, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.read()), 0)

    def test_time_conversion(self):
        time_string1 = '2020-10-17T02:56:51+0700'
        time_string2 = '2020-10-17T02:56:51+07:00'
        utc_string = '2020-10-16 19:56:51+00:00'
        self.assertEqual(convertToUTC(time_string1), utc_string)
        self.assertEqual(convertToUTC(time_string2), utc_string)

    def test_time_invalid(self):
        fixture = self.fixtures[1]
        obj = self.load_fixture(fixture)
        self.assertFalse(process_time(obj))
        
        # assert output file length
        main(['-i', fixture, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.read()), 0)

    def test_json_invalid(self):
        fixture = self.fixtures[2]
        with open(fixture) as f:
            self.assertIsNone(load_json(f.readline()))
        
        # assert output file length
        main(['-i', fixture, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.read()), 0)

    def test_author_invalid(self):
        fixture = self.fixtures[3]
        obj = self.load_fixture(fixture)
        self.assertFalse(process_author(obj))

        # assert output file length
        main(['-i', fixture, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.read()), 0)

    def test_total_count_invalid(self):
        fixture = self.fixtures[4]
        obj = self.load_fixture(fixture)
        self.assertFalse(process_total_count(obj))

        # assert output file length
        main(['-i', fixture, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.read()), 0)

    def test_tags_with_three_words(self):
        fixture = self.fixtures[5]
        obj = self.load_fixture(fixture)
        og_len = len(obj['tags'])
        self.assertTrue(process_tags(obj))
        self.assertEqual(len(obj['tags']), 2 + og_len)

        # assert output file length
        main(['-i', fixture, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.readlines()), 1)

    def test_load_success(self):
        s = '{"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "druths", "total_count": "12"}'
        self.assertIsNotNone(load_json(s))

    def test_output_valid(self):
        s = '{"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "druths", "total_count": "12"}'
        obj = json.loads(s)
        self.assertTrue(process_title(obj))
        self.assertTrue(process_author(obj))
        self.assertTrue(process_time(obj))
        self.assertTrue(process_tags(obj))
        self.assertTrue(process_total_count(obj))

        with open(self.TEST_IN, 'w') as f:
            f.write(s)
        main(['-i', self.TEST_IN, '-o', self.TEST_OUT])
        with open(self.TEST_OUT) as f:
            self.assertEqual(len(f.readlines()), 1)


if __name__ == '__main__':
    unittest.main()
