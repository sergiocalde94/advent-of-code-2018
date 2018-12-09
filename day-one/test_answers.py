import unittest
import frequency_fixer


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        self.assertEqual(frequency_fixer
                         .answer_function_part_one('test_input_one.txt'), 3)

    def test_answer_two_a(self):
        self.assertEqual(frequency_fixer
                         .answer_function_part_two('test_input_two_a.txt'), 0)

    def test_answer_two_b(self):
        self.assertEqual(frequency_fixer
                         .answer_function_part_two('test_input_two_b.txt'), 10)

    def test_answer_two_c(self):
        self.assertEqual(frequency_fixer
                         .answer_function_part_two('test_input_two_c.txt'), 5)

    def test_answer_two_d(self):
        self.assertEqual(frequency_fixer
                         .answer_function_part_two('test_input_two_d.txt'), 14)


if __name__ == '__main__':
    unittest.main()
