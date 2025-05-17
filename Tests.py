import unittest
from main import generate_solved_board, create_puzzle, is_valid, solve_board



class TestSudokuGame(unittest.TestCase):
   
   #Test case 1: testing board generation
    def test_generate_solve_board(self):
    # Testing the generation of the solved Sudoku board.

        #Testing 4x4 board
        board_4x4 = generate_solved_board(4)
        self.assertEqual(len(board_4x4), 4) #assert row has only 4 rows
        self.assertTrue(all(len(row) == 4 for row in board_4x4)) #each row in the board as 4 elemnts

        #generate 9x9 board and also check the size
        board_9x9 = generate_solved_board(9) 
        self.assertEqual(len(board_9x9), 9) # board has 9 rows
        self.assertTrue(all(len(row) == 9 for row in board_9x9)) #each row in the board as 9 elemnts


      #Test case 2: testing puzzle generation
    def test_create_puzzle(self):

        #Testing creating of the sudoku puzzle from solved board
        solve_board_4x4 = generate_solved_board(4) #create solved board 4x4
        puzzle_4x4 = create_puzzle(solve_board_4x4, 8) #generate a puzzle by removing 8 blanks from the solved board
        blank_count = sum(row.count(0) for row in puzzle_4x4) # count number of blanks which are th 0s in the puzzle
        self.assertEqual(blank_count, 8) #here the assert is set to 8 exact blanks
        solve_board_9x9 = generate_solved_board(9) #solve board for 9x9 board
        puzzle_9x9 = create_puzzle(solve_board_9x9, 30)  # this code removes 40 blanks
        blank_count = sum(row.count(0) for row in puzzle_9x9) #count the blanks which are the 0s 
        self.assertEqual(blank_count, 30) #there are 30 blanks (0s)

    # Test case 3: testing valid logic
    def test_is_valid(self): #function

        #EXAMPLE 4X4 SUDOKU BOARD   

        board = [
            [5, 3, 0, 0],
            [6, 0, 0, 0],
            [0, 9, 8, 0],
            [0, 0, 0, 0],
        ]
        # TESTING PLACES SO 4 AT ROW 0, column 2 should be vaild. 
        self.assertTrue(is_valid(board, 0, 2, 4))
        self.assertFalse(is_valid(board, 0, 2, 5)) # testing places 5 at row 0, column 2 shoud be invalid because it exist in row
        self.assertFalse(is_valid(board, 2, 0, 6)) # testing places 6 at row 2, column 0 shoud be invalid because it exist in column
        
  #Test case 4: testing board solvie logic

    def test_solve_board(self):
        board_4x4 = [ #unsolved 4x4 board
            [1, 0, 0, 4],
            [0, 0, 4, 0],
            [3, 4, 0, 0],
            [0, 0, 1, 3]
        ]

        solve_board(board_4x4)
        print("board before solving 4x4:")
        for row in board_4x4:
            print(row)

        #board is solvable
        self.assertFalse(solve_board(board_4x4))
       


        
if __name__ == '__main__':
    unittest.main()  