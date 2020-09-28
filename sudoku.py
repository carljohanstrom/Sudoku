import argparse




class Sudoku :

    def __init__(self) :
        self.sudoku = None
        self.possible_values = None

    def load_from_file(self, path) :
        sud = []
        try :
            with open(path) as f :
                data = f.readlines()
            for line in data :
                row = [0 if c=="." else int(c) for c in line if c!='\n'] 
                sud.append(row)
        except :
            print("ERROR: could not load the sudoku file.")
        self.sudoku = sud

    def __str__(self) :
        s = ""
        for row in self.sudoku :
            for n in row :
                s+=((str(n) if n!=0 else ".") + " ")
            s+="\n"
        return s

    def possible_to_place(self,y,x,n) :
        for i in range(9) :
            if n == self.sudoku[y][i] : 
                return False
            if n == self.sudoku[i][x] : 
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(3) :
            for j in range(3) :
                if self.sudoku[y0+i][x0+j] == n :
                    return False
        return True

    def find_empty(self) :
        for y in range(9) :
            for x in range(9) :
                if self.sudoku[y][x] == 0 :
                    return y,x
        return None

def _rec_solve(s) :
    found_pos = s.find_empty()
    if not found_pos :
        # we found solution so sudoku must be finished
        return True
    (y,x) = found_pos
    for n in range(1,10) :
        if s.possible_to_place(y,x,n) :
            s.sudoku[y][x] = n
            # recursion
            if _rec_solve(s) :
                return True
            # trick here: backtrack if recursion fails to find terminate (find solution)
            s.sudoku[y][x] = 0
    return False

def solve(s) :
    _rec_solve(s)

if __name__ == "__main__" :
    # (the following is NOT executed if this file is imported in another Python file)

    # MAIN

    parser = argparse.ArgumentParser(description='Python script to solve sudokus. Created by <carljohanstrom@gmail.com>, version 0.1, 2020-09-23.')
    parser.add_argument('input_file', type=str, help="Input filename. One sudoku per file.")
    args = parser.parse_args()
    input_file = args.input_file

    sudoku = Sudoku()

    sudoku.load_from_file(input_file)
    print(sudoku)

    print("Solving...")
    solve(sudoku)

    print(sudoku)



