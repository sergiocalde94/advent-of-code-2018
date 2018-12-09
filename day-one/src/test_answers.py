import unittest
import frequency_fixer


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        filename = '../data/test_input_one.txt'
        self.assertEqual(frequency_fixer
                         .answer_function_part_one(filename), 3)

    def test_answer_two_a(self):
        filename = '../data/test_input_two_a.txt'
        self.assertEqual(frequency_fixer
                         .answer_function_part_two(filename), 0)

    def test_answer_two_b(self):
        filename = '../data/test_input_two_b.txt'
        self.assertEqual(frequency_fixer
                         .answer_function_part_two(filename), 10)

    def test_answer_two_c(self):
        filename = '../data/test_input_two_c.txt'
        self.assertEqual(frequency_fixer
                         .answer_function_part_two(filename), 5)

    def test_answer_two_d(self):
        filename = '../data/test_input_two_d.txt'
        self.assertEqual(frequency_fixer
                         .answer_function_part_two(filename), 14)


if __name__ == '__main__':
    unittest.main()

