import unittest

from domain.board import Board
from repository.board_repo import BoardRepository

class TestBoardRepository(unittest.TestCase):

    def setUp(self):
        self.repo = BoardRepository()
        self.board = Board()

    def test_add_user_plane(self):
        plane = [(1,1), (2,1), (3,1)]
        self.repo.add_user_plane(plane)
        self.assertEqual(len(self.repo.user_planes), 1)
        self.assertEqual(self.repo.user_planes[0], plane)
        from domain import board
        self.assertEqual(self.repo.user_board.get(1,1), Board.PLANE)

    def test_add_computer_plane(self):
        plane = [(1,1), (2,1), (3,1)]
        self.repo.add_computer_plane(plane)
        self.assertEqual(len(self.repo.computer_planes), 1)
        self.assertEqual(self.repo.computer_planes[0], plane)
        self.assertEqual(self.repo.computer_board.get(1,1), Board.PLANE)

    def test_record_user_hit(self):
        self.repo.record_user_hit((3,3))
        self.assertIn((3,3), self.repo.user_hits)

    def test_user_miss(self):
        self.repo.record_user_miss((3,3))
        self.assertIn((3,3), self.repo.user_misses)

    def test_record_computer_hit(self):
        self.repo.record_computer_hit((3,3))
        self.assertIn((3,3), self.repo.computer_hits)

    def test_record_computer_miss(self):
        self.repo.record_computer_miss((3,3))
        self.assertIn((3,3), self.repo.computer_misses)

    def test_all_heads_destroyed(self):
        plane = [(1,1), (1,2)]
        self.repo.user_planes.append(plane)
        self.repo.computer_hits.add((1,1))
        self.assertTrue(self.repo.all_user_heads_destroyed())

    def test_overlapping(self):
        plane1 = [(2,2), (2,3)]
        plane2 = [(2,3), (3,3)]
        self.repo.add_user_plane(plane1)
        self.assertTrue(self.repo.user_plane_overlaps(plane2))



