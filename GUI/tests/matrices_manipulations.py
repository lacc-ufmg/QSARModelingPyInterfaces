import unittest
import os

import Utils


def get_file_path(name: str) -> str:
    dot = os.path.abspath(os.path.dirname(__file__))
    return os.path.realpath(os.path.join(dot, "matrices", name))

class TestHeaderAndIndexDetection(unittest.TestCase):
    def test_header_and_index(self):
        file = get_file_path("header_and_index.csv")
        index, header = Utils.detect_header_and_indices(file)
        self.assertEqual(index, 0)
        self.assertEqual(header, 0)

    def test_header_and_index_with_first_cell(self):
        file = get_file_path("header_and_index_with_first_cell.csv")
        index, header = Utils.detect_header_and_indices(file)
        self.assertEqual(index, 0)
        self.assertEqual(header, 0)

    def test_only_data(self):
        file = get_file_path("only_data.csv")
        index, header = Utils.detect_header_and_indices(file)
        self.assertIsNone(index)
        self.assertIsNone(header)

    def test_only_header(self):
        file = get_file_path("only_header.csv")
        index, header = Utils.detect_header_and_indices(file)
        self.assertEqual(header, 0)
        self.assertIsNone(index)

    def test_only_index(self):
        file = get_file_path("only_index.csv")
        index, header = Utils.detect_header_and_indices(file)
        self.assertEqual(index, 0)
        self.assertIsNone(header)

    def test_numeric_index(self):
        file = get_file_path("numeric_index.csv")
        index, header = Utils.detect_header_and_indices(file)
        self.assertEqual(index, 0)
        self.assertEqual(header, 0)
