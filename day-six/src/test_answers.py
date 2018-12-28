import unittest
import coordinates


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        filename = '../data/test_input.txt'
        self.assertEqual(coordinates
                         .answer_function_part_one(filename), 17)

    def test_answer_two(self):
        filename = '../data/test_input.txt'
        self.assertEqual(coordinates
                         .answer_function_part_two(filename, 32), 16)


if __name__ == '__main__':
    unittest.main()

