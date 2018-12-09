import unittest
import inventory_management


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        filename = '../data/test_input_one.txt'
        self.assertEqual(inventory_management
                         .answer_function_part_one(filename), 12)

    def test_answer_two_a(self):
        filename = '../data/test_input_two.txt'
        self.assertEqual(inventory_management
                         .answer_function_part_two(filename), 'fgij')


if __name__ == '__main__':
    unittest.main()

