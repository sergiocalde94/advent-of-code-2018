import unittest
import guards_sleeping


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        filename_input = '../data/test_input.txt'
        filename_output = '../data/test_input.csv'
        self.assertEqual(guards_sleeping
                         .answer_function_part_one(filename_input, filename_output), 240)

    def test_answer_two_a(self):
        filename_input = '../data/test_input.txt'
        filename_output = '../data/test_input.csv'
        self.assertEqual(guards_sleeping
                         .answer_function_part_two(filename_input, filename_output), 4455)


if __name__ == '__main__':
    unittest.main()
