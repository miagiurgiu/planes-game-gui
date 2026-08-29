class Validation:
    #def __init__(self, coord):

    def validate_coordinates(self, coordinates):
        '''
        Validates a board coordinate.
            - checks format (letter + number)
            - ensures row is between A and J
            - ensures column is between 1 and 10
        :param coordinates:
        :return:
        '''
        if len(coordinates) <2:
            return False
        if coordinates[0] < 'A' or coordinates[0] > 'J':
            return False
        if not coordinates[1:].isdigit():
            return False
        col = int(coordinates[1:])
        if 1<=col<=10:
            return True
        return False