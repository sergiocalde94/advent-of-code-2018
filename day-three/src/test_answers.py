import unittest
import overlap


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        filename = '../data/test_input.txt'
        self.assertEqual(overlap
                         .answer_function_part_one(filename), 4)

    def test_answer_two_a(self):
        filename = '../data/test_input.txt'
        self.assertEqual(overlap
                         .answer_function_part_two(filename), 3)


if __name__ == '__main__':
    unittest.main()

