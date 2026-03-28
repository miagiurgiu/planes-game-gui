import unittest
from domain.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_headers(self):
        self.assertEqual(self.board.get(0,0), ' ')
        self.assertEqual(self.board.get(0,1), 1)
        self.assertEqual(self.board.get(1,0), 'A')
        self.assertEqual(self.board.get(10,0), 'J')

    def test_set_plane(self):
        self.board.set_plane(3,4)
        self.assertEqual(self.board.get(3,4), Board.PLANE)

    def test_set_hit(self):
        self.board.set_hit(5,6)
        self.assertEqual(self.board.get(5,6), Board.HIT)

    def test_set_miss(self):
        self.board.set_miss(2,2)
        self.assertEqual(self.board.get(2,2), Board.MISS)

    def test_in_bounds(self):
        self.assertTrue(self.board.in_bounds(1,1))
        self.assertTrue(self.board.in_bounds(10,10))
        self.assertFalse(self.board.in_bounds(0,1))
        self.assertFalse(self.board.in_bounds(11,5))