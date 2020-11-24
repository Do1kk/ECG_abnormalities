import unittest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # Change dir to parent.
import csv_ann_type


class TestMethods(unittest.TestCase):
    def test_one_beat_len(self):
        self.assertEqual(csv_ann_type.range_len, 260)

    def test_is_shift_used(self):
        self.assertLess(csv_ann_type.L_side, csv_ann_type.R_side)

    def test_every_type_of_beat(self):
        self.assertCountEqual(list(csv_ann_type.beat_ann), list("NLRAaJSVFejE/fQ"))

    def test_sign_not_good_to_name_file(self):
        self.assertNotIn("/", csv_ann_type.beat_ann_file)


if __name__ == "__main__":
    unittest.main()
