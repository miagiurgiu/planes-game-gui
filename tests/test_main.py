import unittest
from repository.board_repo import BoardRepository
from service.board_service import BoardService
from validation.validation import Validation

class TestMain(unittest.TestCase):

    def test_components_creation(self):
        repo = BoardRepository()
        service = BoardService(repo)
        validation = Validation()

        self.assertIsNotNone(repo)
        self.assertIsNotNone(service)
        self.assertIsNotNone(validation)
