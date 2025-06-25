
## Prerequisites

To run this project, you need to have Python installed on your system. The application is built using standard Python libraries and `customtkinter`.

*   **Python:** Version 3.6 or higher is recommended.
*   **Python Libraries:** Install the required libraries using pip:
    ```bash
    pip install customtkinter Pillow imageio numpy
    ```
    *   `customtkinter`: For the modern GUI.
    *   `Pillow` (PIL): For image manipulation and drawing.
    *   `imageio`: For reading and writing image files.
    *   `numpy`: For efficient matrix operations (representing the maze).
*   **Tkinter:** `tkinter` is usually bundled with standard Python distributions. If not, you may need to install it separately depending on your OS.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
    *(Replace `YOUR_USERNAME/YOUR_REPOSITORY_NAME` with your actual GitHub repository path)*

2.  **Install dependencies:** Make sure you have met the [Prerequisites](#prerequisites) and installed the required Python libraries as shown above.

## Usage

1.  **Run the application:**
    ```bash
    python AI.py
    ```
2.  **Use the "Load Image" Tab:**
    *   Click the "Select Maze Image" button and choose a PNG file representing your maze.
    *   White pixels in the image will be treated as traversable paths (value 1), and other colors (ideally black) as walls (value 0).
    *   The application will attempt to find the first and last white pixels as the start and end points.
    *   Click "Pick Color" to choose the color for the solved path visualization.
    *   The input and solved mazes will be displayed side-by-side.
    *   The solved maze image with the path overlaid will be saved in the same directory as the original image file, with `_output_astar` appended to the filename.
3.  **Use the "Draw Maze" Tab:**
    *   Use the "Draw (White)" button to draw the traversable path and the "Erase (Black)" button to draw walls.
    *   Adjust the "Brush Size" slider to change the drawing thickness.
    *   Click "Clear Canvas" to start over.
    *   Click "Pick Color" to choose the path color (shared with the "Load Image" tab).
    *   Click "Solve Maze" to run the A* algorithm on your drawn maze. The first white pixel drawn is the start, and the last is the end.
    *   The solved maze will be displayed on the output canvas below the drawing area.
    *   The solved drawn maze image will be saved to your user's home directory (e.g., `~/drawn_maze_output.png`).

## How it Works

1.  **Maze Representation:** The maze image (loaded or drawn) is converted into a 2D NumPy array. White pixels are mapped to `1` (passable), and other pixels (black or any non-white in the loaded image) are mapped to `0` (impassable).
2.  **Start and Goal:** The algorithm identifies the first and last white pixels encountered when scanning the maze array as the start and goal positions.
3.  **A* Algorithm:**
    *   A* explores the maze grid by evaluating potential paths based on two costs: `g` (the cost from the start node to the current node) and `h` (the estimated cost from the current node to the goal node - the heuristic).
    *   Here, `g` is the number of steps taken (each step costs 1), and `h` is the Manhattan distance (sum of the absolute differences of x and y coordinates) to the goal.
    *   It uses a priority queue (`heapq`) to always explore the node with the lowest total cost (`g + h`).
    *   It keeps track of visited nodes (`closed_set`) to avoid infinite loops and redundant paths.
4.  **Path Reconstruction:** Once the goal is reached, the algorithm backtracks from the goal node to the start node using the parent pointers stored in each node, reconstructing the shortest path.
5.  **Visualization:** The calculated path coordinates are used to draw pixels (or small rectangles for drawn mazes) of the chosen color onto a copy of the original image.

## Future Improvements

*   **Click-to-Select Start/End:** Allow users to click on the maze to specify the start and end points instead of relying on the first/last white pixels.
*   **Larger Maze Support:** Optimize image scaling and potentially the A* implementation for handling very large maze images.
*   **Different Heuristics:** Implement and compare different heuristic functions for the A* algorithm (e.g., Euclidean distance).
*   **More Maze Formats:** Add support for loading other image formats or different maze representations (e.g., colored start/end points).
*   **Add Other Algorithms:** Include implementations of other pathfinding algorithms like Dijkstra's, Breadth-First Search (BFS), or Depth-First Search (DFS) for comparison.
*   **Performance Analysis:** Add tools to measure the time taken by the algorithm for different maze sizes.
*   **Error Handling:** Improve error handling for edge cases (e.g., no path exists, invalid start/end).
*   **Refined Drawing:** Add more sophisticated drawing tools or options for creating drawn mazes.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

If you have any questions or feedback, please open an issue on this GitHub repository.

---
