import argparse
import sys



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
            sys.exit(0)
        self.sudoku = sud

    def __str__(self) :
        s = ""
        for row in self.sudoku :
            for n in row :
                s+=((str(n) if n!=0 else ".") + " ")
            s+="\n"
        return s

    def possible_to_place(self, y, x, n) :
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


    def cell_possibilities(self, y, x) :
        cell_possible = [1,2,3,4,5,6,7,8,9]
        for i in range(9) :
            try :
                cell_possible.remove(self.sudoku[y][i])
            except :
                pass
            try :
                cell_possible.remove(self.sudoku[i][x])
            except :
                pass
        if cell_possible == [] : return cell_possible # just optimization
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(3) :
            for j in range(3) :
                try :
                    cell_possible.remove(self.sudoku[y0+i][x0+j])
                    if cell_possible == [] : return [] # just optimization
                except :
                    pass
        return cell_possible


    def best_empty_pos_and_number(self) :
        solved = True
        unfilled_cells = []
        for y in range(9) :
            for x in range(9) :
                if self.sudoku[y][x] == 0 :
                    solved = False
                    poss = self.cell_possibilities(y, x)
                    unfilled_cells.append((y,x,poss))    
        # sort and return first with lowest number of possibilities (but of course not empty possibilities)
        sorted_by_third = sorted(unfilled_cells, key=lambda tup: len(tup[2]))        
        if solved :
            return True
        else :
            return sorted_by_third[0][0],sorted_by_third[0][1],sorted_by_third[0][2]


def solve(sud) :
    result = sud.best_empty_pos_and_number()
    if result == True :
        # we found a solution so sudoku must be finished
        return True
    (y,x,numbers) = result
    # try each of the possibilities (note that loop contains recursion step)
    for n in numbers :
        sud.sudoku[y][x] = n
        # recursion
        if solve(sud) :
            return True
        # trick here: backtrack if recursion fails to find terminate (find solution)
        sud.sudoku[y][x] = 0
    return False


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



