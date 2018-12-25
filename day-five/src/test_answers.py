import unittest
import alchemical_reduction


class TestAnswers(unittest.TestCase):

    def test_answer_one_a(self):
        filename = '../data/test_input_one_a.txt'
        self.assertEqual(alchemical_reduction
                         .answer_function_part_one(filename), 0)

    def test_answer_one_b(self):
        filename = '../data/test_input_one_b.txt'
        self.assertEqual(alchemical_reduction
                         .answer_function_part_one(filename), 0)

    def test_answer_one_c(self):
        filename = '../data/test_input_one_c.txt'
        self.assertEqual(alchemical_reduction
                         .answer_function_part_one(filename), 4)

    def test_answer_one_d(self):
        filename = '../data/test_input_one_d.txt'
        self.assertEqual(alchemical_reduction
                         .answer_function_part_one(filename), 6)

    def test_answer_one_e(self):
        filename = '../data/test_input_one_e.txt'
        self.assertEqual(alchemical_reduction
                         .answer_function_part_one(filename), 10)

    def test_answer_two(self):
        filename = '../data/test_input_one_e.txt'
        self.assertEqual(alchemical_reduction
                         .answer_function_part_two(filename), 4)


if __name__ == '__main__':
    unittest.main()
