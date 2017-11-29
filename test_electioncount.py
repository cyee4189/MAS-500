import unittest
import electioncount

class ElectionCountTest(unittest.TestCase):

    def test_TrumpCount(self):
        result = electioncount.ElectionCount('Trump')
        self.assertEqual(result, 33660)