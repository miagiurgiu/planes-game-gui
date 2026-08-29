import unittest
from service.board_service import BoardService
from repository.board_repo import BoardRepository

class TestBoardService(unittest.TestCase):

    def setUp(self):
        self.repo = BoardRepository()
        self.service = BoardService(self.repo)

    def test_parse_coord(self):
        self.assertEqual(self.service._parse_coord("A1"), (1,1))
        self.assertEqual(self.service._parse_coord("J10"), (10,10))

    def test_place_user_plane(self):
        self.service.place_user_planes("A3", "D3")
        self.service.place_user_planes("A9", "D9")
        self.service.place_user_planes("G8", "J8")
        self.assertEqual(len(self.repo.user_planes), 3)

    def test_place_computer_planes(self):
        self.service.place_computer_planes()
        self.assertEqual(len(self.repo.computer_planes), 3)

    def test_user_move_hit(self):
        plane1 = [(3,3), (4,3)]
        plane2 = [(5,3), (6,3)]
        self.repo.computer_planes.append(plane1)
        result1 = self.service.user_move("D3")
        self.assertEqual("you hit!", result1.lower())
        self.repo.computer_planes.append(plane2)
        result2 = self.service.user_move("E3")
        self.assertEqual("head destroyed by you!", result2.lower())

    def test_user_move_already_attacked(self):
        self.repo.user_hits.add((2,2))
        with self.assertRaises(ValueError):
            self.service.user_move("B2")

