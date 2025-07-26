import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def generate_smooth_line(length, num_control_points, max_deviation):
    control_x = np.linspace(0, length-1, num_control_points)
    control_y = np.random.randint(-max_deviation, max_deviation+1, num_control_points)
    
    f = interp1d(control_x, control_y, kind='cubic')
    
    x = np.arange(length)
    return f(x)

def generate_jagged_grid(image_path):
    img = Image.open(image_path)
    width, height = img.size
    
    grid = np.zeros((height, width), dtype=np.int8)
    
    num_horizontal = 5
    vertical_spacing = height // (num_horizontal + 1)
    
    num_control_points = 10
    
    for i in range(1, num_horizontal + 1):
        base_y = i * vertical_spacing
        deviations = generate_smooth_line(width, num_control_points, 45)
        
        for x in range(width):
            y = int(base_y + deviations[x])
            y = min(max(y, 0), height - 1) 
            grid[y, x] = 1
    
    num_vertical = 10
    horizontal_spacing = width // (num_vertical + 1)
    
    for i in range(1, num_vertical + 1):
        base_x = i * horizontal_spacing
        deviations = generate_smooth_line(height, num_control_points, 10)
        
        for y in range(height):
            x = int(base_x + deviations[y])
            x = min(max(x, 0), width - 1)  
            grid[y, x] = 1
    
    return grid

def display_grid(grid):
  
    
    #MATPLOTLIB 
    plt.figure(figsize=(12, 8))
    plt.imshow(grid, cmap='binary')
    plt.title('Grid Visualization (white = lines, black = empty)')
    plt.axis('on')
    plt.grid(True, which='both', color='gray', linewidth=0.5, alpha=0.3)
    plt.show()
    
    print("\nGrid shape:", grid.shape)

if __name__ == "__main__":
    image_path = input("Enter the path to your image: ")
    grid = generate_jagged_grid(image_path)
    display_grid(grid) 