import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from bofpy.BofStatistics import (                                                           
    BofStatVariable
)

class TestBofStatVariable(unittest.TestCase):

    def test_reset_stat_var(self):
        stat_var = BofStatVariable()

        # Set initial values
        stat_var.crt = 5
        stat_var.min = 2
        stat_var.max = 8
        stat_var.mean = 6.5
        stat_var.mean_acc = 13
        stat_var.nb_sample = 2

        # Reset the statistics
        stat_var.Bof_ResetStatVar()

        # Check if the values are reset to their initial state
        self.assertEqual(stat_var.crt, 0)
        self.assertEqual(stat_var.min, sys.maxsize)
        self.assertEqual(stat_var.max, -sys.maxsize-1)
        self.assertEqual(stat_var.mean, 0)
        self.assertEqual(stat_var.mean_acc, 0)
        self.assertEqual(stat_var.nb_sample, 0)

    def test_update_stat_var_first_sample(self):
        stat_var = BofStatVariable()

        # Update with the first sample
        stat_var.Bof_UpdateStatVar(10)

        # Check if values are updated correctly for the first sample
        self.assertEqual(stat_var.crt, 10)
        self.assertEqual(stat_var.min, 10)
        self.assertEqual(stat_var.max, 10)
        self.assertEqual(stat_var.mean, 10)
        self.assertEqual(stat_var.mean_acc, 10)
        self.assertEqual(stat_var.nb_sample, 1)

    def test_update_stat_var_multiple_samples(self):
        stat_var = BofStatVariable()

        # Update with multiple samples
        stat_var.Bof_UpdateStatVar(5)
        stat_var.Bof_UpdateStatVar(15)
        stat_var.Bof_UpdateStatVar(8)

        # Check if values are updated correctly for multiple samples
        self.assertEqual(stat_var.crt, 8)
        self.assertEqual(stat_var.min, 5)
        self.assertEqual(stat_var.max, 15)
        self.assertEqual(stat_var.mean, (5 + 15 + 8) / 3)
        self.assertEqual(stat_var.mean_acc, 28)
        self.assertEqual(stat_var.nb_sample, 3)

    def test_update_stat_var_roll_over(self):
        stat_var = BofStatVariable()

        # Update with values that cause mean accumulator roll-over
        stat_var.mean_acc = sys.maxsize - 5
        stat_var.Bof_UpdateStatVar(10)

        # Check if values are updated correctly after roll-over
        self.assertEqual(stat_var.mean_acc, stat_var.mean)
        self.assertEqual(stat_var.nb_sample, 1)

if __name__ == "__main__":
    unittest.main()
