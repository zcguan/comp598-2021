import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
import src.compile_word_counts
import src.compute_pony_lang


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.output_word_counts = os.path.join(os.path.dirname(__file__), 'test_output.json')
        
    def tearDown(self):
        if os.path.isfile(self.output_word_counts):
            os.remove(self.output_word_counts)

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        args = ['-o', self.output_word_counts, '-d', self.mock_dialog]
        src.compile_word_counts.main(args)
        with open(self.output_word_counts) as f:
            actual = json.load(f)
        with open(self.true_word_counts) as f:
            expected = json.load(f)
        self.assertEqual(expected, actual)

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        args = ['-c', self.true_word_counts, '-n', '10']
        actual = src.compute_pony_lang.main(args, True)
        with open(self.true_tf_idfs) as f:
            expected = json.load(f)
        self.assertEqual(expected, actual)
        
    
if __name__ == '__main__':
    unittest.main()
