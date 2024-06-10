/**
  localizer.cpp

  Goal of this file: implements a 2-dimensional histogram filter
  for a robot living on a colored cyclical grid by
  correctly implementing the "initialize_beliefs",
  "sense", and "move" functions.
*/

#include "localizer.h"
#include "helpers.cpp"
#include <stdlib.h>
#include "debugging_helpers.cpp"
using namespace std;\
/**
  TODO - implement this function

    Initializes a grid of beliefs to a uniform distribution.

    @param grid - a two dimensional grid map (vector of vectors
         of chars) representing the robot's world. For example:

         g g g
         g r g
         g g g

       would be a 3x3 world where every cell is green except
       for the center, which is red.

    @return - a normalized two dimensional grid of floats. For
           a 2x2 grid, for example, this would be:

           0.25 0.25
           0.25 0.25
*/
vector<vector<float>> initialize_beliefs(vector<vector<char>> grid)
{
  vector<vector<float>> newGrid;

  // Declaration of variables and belief
  int height = grid.size();
  int width = grid[0].size();
  int area = height * width;
  float belief = 1.0 / area;

  for (int i = 0; i < height; i++)
  {
    vector<float> row;
    for (int j = 0; j < width; j++)
    {
      row.push_back(belief); // Push belif in one cell
    }
    newGrid.push_back(row);
  }

  // Your code here:

  return newGrid;
}

/**
  TODO - implement this function

    Implements robot motion by updating beliefs based on the
    intended dx and dy of the robot.

    For example, if a localized robot with the following beliefs

    0.00  0.00  0.00
    0.00  1.00  0.00
    0.00  0.00  0.00

    and dx and dy are both 1 and blurring is 0 (noiseless motion),
    than after calling this function the returned beliefs would be

    0.00  0.00  0.00
    0.00  0.00  0.00
    0.00  0.00  1.00

  @param dy - the intended change in y position of the robot

  @param dx - the intended change in x position of the robot

    @param beliefs - a two dimensional grid of floats representing
         the robot's beliefs for each cell before sensing. For
         example, a robot which has almost certainly localized
         itself in a 2D world might have the following beliefs:

         0.01 0.98
         0.00 0.01

    @param blurring - A number representing how noisy robot motion
           is. If blurring = 0.0 then motion is noiseless.

    @return - a normalized two dimensional grid of floats
         representing the updated beliefs for the robot.
*/
vector<vector<float>> move(int dy, int dx,
                           vector<vector<float>> beliefs,
                           float blurring)
{

  vector<vector<float>> newGrid;

  // Get grid height and width
  int height = beliefs.size();
  int width = beliefs[0].size();
  newGrid = zeros(height, width); // Declare new grid with height and width

  // your code here

  for (int row = 0; row < beliefs.size(); row++)
  {
    for (int col = 0; col < beliefs.size(); col++)
    {
      int new_row = (row + dy + height) % height;
      int new_column = (col + dx + width) % width;
      newGrid[new_row][new_column] = beliefs[row][col]; // Assigne belif to new_row and new_column
    }
  }
  // Your code here:
  return blur(newGrid, blurring);
}

/**
  TODO - implement this function

    Implements robot sensing by updating beliefs based on the
    color of a sensor measurement

  @param color - the color the robot has sensed at its location

  @param grid - the current map of the world, stored as a grid
       (vector of vectors of chars) where each char represents a
       color. For example:

       g g g
         g r g
         g g g

    @param beliefs - a two dimensional grid of floats representing
         the robot's beliefs for each cell before sensing. For
         example, a robot which has almost certainly localized
         itself in a 2D world might have the following beliefs:

         0.01 0.98
         0.00 0.01

    @param p_hit - the RELATIVE probability that any "sense" is
         correct. The ratio of p_hit / p_miss indicates how many
         times MORE likely it is to have a correct "sense" than
         an incorrect one.

    @param p_miss - the RELATIVE probability that any "sense" is
         incorrect. The ratio of p_hit / p_miss indicates how many
         times MORE likely it is to have a correct "sense" than
         an incorrect one.

    @return - a normalized two dimensional grid of floats
         representing the updated beliefs for the robot.
*/
vector<vector<float>> sense(char color,
                            vector<vector<char>> grid,
                            vector<vector<float>> beliefs,
                            float p_hit,
                            float p_miss)
{

  // Get grid height and width
  int height = beliefs.size();
  int width = beliefs[0].size();
  int row, col;
  vector<vector<float>> newGrid = zeros(height, width);

  for (row = 0; row < height; row++)
  {
    for (col = 0; col < width; col++)
    {
      newGrid[row][col] = beliefs[row][col];
      if (grid[row][col] == color)
      {
        newGrid[row][col] *= p_hit;
      }
      else
      {
        newGrid[row][col] *= p_miss;
      }
    }
  }

  // your code here

  return normalize(newGrid);
}