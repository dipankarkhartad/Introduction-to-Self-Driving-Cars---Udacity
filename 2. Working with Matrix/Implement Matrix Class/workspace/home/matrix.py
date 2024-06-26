import math
import numbers
from math import sqrt

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I
 
 
def dot_product(vector_one, vector_two):
    if(len(vector_one)!=len(vector_two)):
        return
    else:
#        product = 0
#        for i in range(len(vector_one)):
#            product = product + vector_one[i]*vector_two[i]
        product_list = [vector_one[i]*vector_two[i] for i in range(len(vector_one))]
    return sum(product_list)
    
class Matrix:

    def __init__(self, grid) -> None:
        """constructor"""
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    def is_square(self):
        """Check squar matrix"""
        return self.h == self.w
    
    def get_row(self,row):
        """Get row"""
        return self.g[row]
    
    def get_column(self,col):
        """get column"""
        return [self.g[row][col] for row in range(self.h)]
    


    def determinant(self):
        """Calculate determinant of the matrix"""
        if not self.is_square():
            raise (ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise (NotImplemented, "Not implemented if size >2.")

        if self.is_square() and self.h == 1:
            return self.g[0][0]
        elif self.is_square() and self.h == 2:
            dt = self.g[0][0] * self.g[1][1] - self.g[0][1] * self.g[1][0]
            return dt

    def trace(self):
        """calculate the trace of matrix, sum of diagonal entries"""
        if not self.is_square():
            raise (ValueError, "Cannot calculate the trace as its not squar matrix")
        else:
            sum = 0
            for row in range(self.h):
                for col in range(self.w):
                    if row == col:
                        sum = sum + self.g[row][col]
            return sum

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        inverse = []
        if not self.is_square():
            raise (ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise (
                NotImplementedError,
                "inversion not implemented for matrices larger than 2x2.",
            )

        if self.h == 1:
            inverse = zeroes(1,1)
            inverse[0][0] = 1 / self.g[0][0]
            return inverse
        elif self.h == 2:
            if self.determinant() == 0:
                raise (ValueError, "Cannot calculate inverse.")
            else:
                #  the inverse of the square 1x1 or 2x2 matrix.
                inverse = zeroes(2,2)
                determinant = 1/self.determinant()
                inverse[0][0] = determinant*self.g[1][1]
                inverse[0][1] = -determinant*self.g[0][1]
                inverse[1][0] = -determinant*self.g[1][0]
                inverse[1][1] = determinant*self.g[0][0]
                return inverse
                
    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        # TODO - your code here
        transpose =  zeroes(self.w,self.h)
        for j in range(self.w):
            for i in range(self.h):
                transpose[j][i] = self.g[i][j]
        return transpose
    
        # return [[self.g[row][col] for row in range(self.h)] for col in range(self.w)]
    
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]
        > my_matrix[0][0]
          1
        """
        return self.g[idx]
    
    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s
    
    def __add__(self, other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise (
                ValueError,
                "Matrices can only be added if the dimensions are the same",
            )
        #
        # TODO - your code here
        #
        final = zeroes(self.h,self.w)
        for row in range(self.h):
            for col in range(self.w):
                final[row][col] = self.g[row][col]+other.g[row][col]
        return final
    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        #
        # TODO - your code here
        #
        neg = zeroes(self.h,self.w)
        for i in range(self.h):
            for j in range(self.w):
                neg[i][j] = -1 * self.g[i][j]
        return neg

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #
        # TODO - your code here
        #
        sub = zeroes(self.h,self.w)
        for i in range(self.h):
            for j in range(self.w):
                sub[i][j] = self.g[i][j]-other.g[i][j]
        return sub
    
    
    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        #
        # TODO - your code here
        #
        if self.w!=other.h:
            raise (ValueError, " for nxm and oxp matrix m==o")
        else:
            mul = zeroes(self.h,other.w)
            for row in range(self.h):
                one_row = []
                for col in range(other.w):
                    mul[row][col] = dot_product(self.get_row(row),other.get_column(col))        
            return mul
        
        

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            rmulti = zeroes(self.h, self.w)
            for i in range(self.h):
                for j in range(self.w):
                    rmulti[i][j] = self.g[i][j] * other
            return rmulti