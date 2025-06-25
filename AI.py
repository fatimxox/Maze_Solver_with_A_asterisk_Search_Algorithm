import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw
import imageio.v2 as imageio
import numpy as np
import heapq
import os

# Set customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Node:
    def __init__(self, x, y, g=float('inf'), h=0):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = None

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

def a_star(maze, start_pos, goal_pos, width, height):
    open_set = []
    closed_set = set()
    start = Node(start_pos[1], start_pos[0], 0, 0)
    goal = Node(goal_pos[1], goal_pos[0], 0, 0)
    
    start.h = abs(start.x - goal.x) + abs(start.y - goal.y)
    heapq.heappush(open_set, (start.g + start.h, start))
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if (current.y, current.x) == goal_pos:
            path = []
            while current:
                path.append((current.y, current.x))
                current = current.parent
            return path[::-1]
        
        closed_set.add(current)
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny, nx] == 1:
                neighbor = Node(nx, ny)
                if neighbor in closed_set:
                    continue
                
                tentative_g = current.g + 1
                
                existing = next((n for n in [item[1] for item in open_set] if n == neighbor), None)
                if not existing or tentative_g < existing.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = abs(nx - goal.x) + abs(ny - goal.y)
                    if not existing:
                        heapq.heappush(open_set, (neighbor.g + neighbor.h, neighbor))
                    else:
                        open_set = [(f, n) for f, n in open_set if n != existing]
                        heapq.heapify(open_set)
                        heapq.heappush(open_set, (neighbor.g + neighbor.h, neighbor))
    
    return None

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver with A* Algorithm")
        self.root.geometry("1200x700")
        
        # Tab view
        self.tab_view = ctk.CTkTabview(self.root)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.image_tab = self.tab_view.add("Load Image")
        self.draw_tab = self.tab_view.add("Draw Maze")
        
        self.path_color = (33, 180, 148)  # Default path color
        self.draw_size = 10  # Brush size for drawing
        
        self.setup_image_tab()
        self.setup_draw_tab()
        
        # Common elements
        self.status_label = ctk.CTkLabel(self.root, text="")
        self.status_label.pack(pady=5)
        
        self.explanation = ctk.CTkLabel(
            self.root,
            text="How it works: The A* algorithm finds the shortest path in a maze using Manhattan distance as a heuristic. "
                 "White pixels are paths (passable), black pixels are walls (impassable). In the 'Load Image' tab, select a maze image "
                 "and choose a path color. In the 'Draw Maze' tab, draw your own maze and click 'Solve Maze' to see the solution.",
            wraplength=1100
        )
        self.explanation.pack(pady=10)
    
    def setup_image_tab(self):
        # Main frame to center content
        self.image_main_frame = ctk.CTkFrame(self.image_tab)
        self.image_main_frame.pack(expand=True, fill="both")
        
        # Image selection
        self.select_button = ctk.CTkButton(
            self.image_main_frame, text="Select Maze Image", command=self.select_image
        )
        self.select_button.pack(pady=10)
        
        # Color picker
        self.color_label = ctk.CTkLabel(self.image_main_frame, text="Path Color:")
        self.color_label.pack()
        self.color_button = ctk.CTkButton(
            self.image_main_frame, text="Pick Color", command=self.choose_color,
            fg_color=f"#{self.path_color[0]:02x}{self.path_color[1]:02x}{self.path_color[2]:02x}"
        )
        self.color_button.pack(pady=5)
        
        # Image display frame
        self.image_frame = ctk.CTkFrame(self.image_main_frame)
        self.image_frame.pack(pady=20, expand=True)
        
        self.input_label = ctk.CTkLabel(self.image_frame, text="Input Maze")
        self.input_label.grid(row=0, column=0, padx=20, pady=5)
        self.output_label = ctk.CTkLabel(self.image_frame, text="Solved Maze")
        self.output_label.grid(row=0, column=1, padx=20, pady=5)
        
        self.input_canvas = ctk.CTkCanvas(self.image_frame, width=400, height=400, bg="black")
        self.input_canvas.grid(row=1, column=0, padx=20, pady=10)
        self.output_canvas = ctk.CTkCanvas(self.image_frame, width=400, height=400, bg="black")
        self.output_canvas.grid(row=1, column=1, padx=20, pady=10)
        
        self.image = None
        self.output_image = None
        self.photo_input = None
        self.photo_output = None
    
    def setup_draw_tab(self):
        # Drawing controls
        self.draw_frame = ctk.CTkFrame(self.draw_tab)
        self.draw_frame.pack(pady=10)
        
        self.draw_button = ctk.CTkButton(
            self.draw_frame, text="Draw (White)", command=lambda: self.set_draw_mode("white")
        )
        self.draw_button.pack(side="left", padx=5)
        
        self.erase_button = ctk.CTkButton(
            self.draw_frame, text="Erase (Black)", command=lambda: self.set_draw_mode("black")
        )
        self.erase_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            self.draw_frame, text="Clear Canvas", command=self.clear_canvas
        )
        self.clear_button.pack(side="left", padx=5)
        
        self.solve_button = ctk.CTkButton(
            self.draw_frame, text="Solve Maze", command=self.solve_drawn_maze
        )
        self.solve_button.pack(side="left", padx=5)
        
        # Color picker for path
        self.draw_color_label = ctk.CTkLabel(self.draw_frame, text="Path Color:")
        self.draw_color_label.pack(side="left", padx=5)
        self.draw_color_button = ctk.CTkButton(
            self.draw_frame, text="Pick Color", command=self.choose_color,
            fg_color=f"#{self.path_color[0]:02x}{self.path_color[1]:02x}{self.path_color[2]:02x}"
        )
        self.draw_color_button.pack(side="left", padx=5)
        
        # Brush size slider
        self.brush_size_label = ctk.CTkLabel(self.draw_frame, text="Brush Size:")
        self.brush_size_label.pack(side="left", padx=5)
        self.brush_size_slider = ctk.CTkSlider(self.draw_frame, from_=5, to=20, command=self.update_brush_size)
        self.brush_size_slider.set(self.draw_size)
        self.brush_size_slider.pack(side="left", padx=5)
        
        # Drawing canvas
        self.draw_canvas = ctk.CTkCanvas(self.draw_tab, width=400, height=400, bg="black")
        self.draw_canvas.pack(pady=10)
        
        # Output canvas
        self.draw_output_canvas = ctk.CTkCanvas(self.draw_tab, width=400, height=400, bg="black")
        self.draw_output_canvas.pack(pady=10)
        
        self.draw_image = Image.new("RGB", (400, 400), "black")
        self.draw_image_pil = self.draw_image
        self.draw_photo = ImageTk.PhotoImage(self.draw_image)
        self.draw_canvas.create_image(200, 200, image=self.draw_photo)
        
        self.draw_mode = "white"
        self.draw_image_draw = ImageDraw.Draw(self.draw_image)
        self.draw_canvas.bind("<B1-Motion>", self.draw)
        self.draw_output_image = None
        self.draw_output_photo = None
    
    def set_draw_mode(self, mode):
        self.draw_mode = mode
    
    def update_brush_size(self, value):
        self.draw_size = int(value)
    
    def draw(self, event):
        x, y = event.x, event.y
        color = "white" if self.draw_mode == "white" else "black"
        self.draw_image_draw.ellipse(
            [x - self.draw_size, y - self.draw_size, x + self.draw_size, y + self.draw_size],
            fill=color
        )
        self.draw_photo = ImageTk.PhotoImage(self.draw_image)
        self.draw_canvas.create_image(200, 200, image=self.draw_photo)
    
    def clear_canvas(self):
        self.draw_image = Image.new("RGB", (400, 400), "black")
        self.draw_image_draw = ImageDraw.Draw(self.draw_image)
        self.draw_photo = ImageTk.PhotoImage(self.draw_image)
        self.draw_canvas.create_image(200, 200, image=self.draw_photo)
        self.draw_output_image = None
        self.draw_output_photo = None
        self.draw_output_canvas.delete("all")
        self.status_label.configure(text="Canvas cleared.")
    
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Path Color")[0]
        if color:
            self.path_color = (int(color[0]), int(color[1]), int(color[2]))
            hex_color = f"#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}"
            self.color_button.configure(fg_color=hex_color)
            self.draw_color_button.configure(fg_color=hex_color)
            if self.image:
                self.process_image(self.current_file)
            if self.draw_output_image:
                self.solve_drawn_maze()
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.status_label.configure(text="Processing...")
            self.root.update()
            self.process_image(file_path)
    
    def process_image(self, file_path):
        self.current_file = file_path
        try:
            img = imageio.imread(file_path)
            if len(img.shape) != 3 or img.shape[2] < 3:
                self.status_label.configure(text="Error: Invalid image format.")
                return
            
            height, width = img.shape[:2]
            maze = np.zeros((height, width), dtype=int)
            
            for y in range(height):
                for x in range(width):
                    maze[y, x] = 1 if img[y, x, 0] == 255 else 0
            
            start = None
            end = None
            for y in range(height):
                for x in range(width):
                    if maze[y, x] == 1:
                        if start is None:
                            start = (y, x)
                        end = (y, x)
            
            if start is None or end is None:
                self.status_label.configure(text="Error: No valid path found in maze.")
                return
            
            path = a_star(maze, start, end, width, height)
            if not path:
                self.status_label.configure(text="Error: No path found.")
                return
            
            output_img = img.copy()
            for y, x in path:
                output_img[y, x, 0] = self.path_color[0]
                output_img[y, x, 1] = self.path_color[1]
                output_img[y, x, 2] = self.path_color[2]
            
            output_path = file_path[:-4] + "_output_astar.png"
            imageio.imwrite(output_path, output_img)
            
            self.image = Image.fromarray(img)
            self.output_image = Image.fromarray(output_img)
            
            # Scale images to fit 400x400 canvas while preserving aspect ratio
            canvas_size = 400
            for img in [self.image, self.output_image]:
                img_width, img_height = img.size
                ratio = min(canvas_size / img_width, canvas_size / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.photo_input = ImageTk.PhotoImage(self.image)
            self.photo_output = ImageTk.PhotoImage(self.output_image)
            
            self.input_canvas.delete("all")
            self.output_canvas.delete("all")
            # Center images on canvas
            self.input_canvas.create_image(200, 200, image=self.photo_input, anchor="center")
            self.output_canvas.create_image(200, 200, image=self.photo_output, anchor="center")
            
            self.status_label.configure(text=f"Path found! Output saved as {output_path}")
        
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
    
    def solve_drawn_maze(self):
        try:
            self.status_label.configure(text="Processing drawn maze...")
            self.root.update()
            
            img_array = np.array(self.draw_image)
            height, width = img_array.shape[:2]
            maze = np.zeros((height, width), dtype=int)
            
            for y in range(height):
                for x in range(width):
                    maze[y, x] = 1 if img_array[y, x, 0] == 255 else 0
            
            start = None
            end = None
            for y in range(height):
                for x in range(width):
                    if maze[y, x] == 1:
                        if start is None:
                            start = (y, x)
                        end = (y, x)
            
            if start is None or end is None:
                self.status_label.configure(text="Error: No valid path found in maze.")
                return
            
            path = a_star(maze, start, end, width, height)
            if not path:
                self.status_label.configure(text="Error: No path found.")
                return
            
            self.draw_output_image = self.draw_image.copy()
            draw = ImageDraw.Draw(self.draw_output_image)
            for y, x in path:
                draw.rectangle(
                    [x - 2, y - 2, x + 2, y + 2],
                    fill=self.path_color
                )
            
            output_path = os.path.join(os.path.expanduser("~"), "drawn_maze_output.png")
            self.draw_output_image.save(output_path)
            
            self.draw_output_image.thumbnail((400, 400))
            self.draw_output_photo = ImageTk.PhotoImage(self.draw_output_image)
            self.draw_output_canvas.delete("all")
            self.draw_output_canvas.create_image(200, 200, image=self.draw_output_photo)
            
            self.status_label.configure(text=f"Path found! Output saved as {output_path}")
        
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MazeSolverApp(root)
    root.mainloop()