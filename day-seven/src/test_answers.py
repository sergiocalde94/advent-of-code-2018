import unittest
import maze


class TestAnswers(unittest.TestCase):

    def test_answer_one(self):
        filename = '../data/test_input.txt'
        self.assertEqual(maze
                         .answer_function_part_one(filename), 'CABDFE')

    def test_answer_two(self):
        filename = '../data/test_input.txt'
        self.assertEqual(maze
                         .answer_function_part_two(filename, 2, 0), 15)


if __name__ == '__main__':
    unittest.main()

