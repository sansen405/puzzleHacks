import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def generate_jagged_line(length, num_control_points, max_deviation):
    control_x = np.linspace(0, length-1, num_control_points)
    control_y = np.zeros(num_control_points)
    for i in range(num_control_points):
        if i > 0:
            prev_y = control_y[i-1]
            control_y[i] = prev_y + np.random.randint(-max_deviation//2, max_deviation//2)
            control_y[i] = np.clip(control_y[i], -max_deviation, max_deviation)
    
    f = interp1d(control_x, control_y, kind='linear')
    x = np.arange(length)
    return f(x)

def generate_jagged_grid(image_path):
    img = Image.open(image_path)
    width, height = img.size
    grid = np.zeros((height, width), dtype=np.int8)
    
    horizontal_sections = 6
    vertical_spacing = height / horizontal_sections
    
    #HORIZONTAL LINES
    num_horizontal = 5
    num_control_points = width // 20
    
    horizontal_positions = []
    for i in range(1, num_horizontal + 1):
        base_y = int(i * vertical_spacing)
        horizontal_positions.append(base_y)
        deviations = generate_jagged_line(width, num_control_points, 25)
        
        for x in range(width):
            y = int(base_y + deviations[x])
            y = min(max(y, 0), height - 1)
            grid[y, x] = 1
    
    #VERTICAL LINES
    vertical_sections = 10
    horizontal_spacing = width / vertical_sections
    num_vertical = 9
    num_control_points_vertical = height // 20
    
    vertical_positions = []
    for i in range(1, num_vertical + 1):
        base_x = int(i * horizontal_spacing)
        vertical_positions.append(base_x)
        deviations = generate_jagged_line(height, num_control_points_vertical, 25)
        
        for y in range(height):
            x = int(base_x + deviations[y])
            x = min(max(x, 0), width - 1)
            grid[y, x] = 1
    
    #CENTERS
    tile_centers = []
    for i in range(len(horizontal_positions) + 1):
        row = []
        y_center = int((i * vertical_spacing) + (vertical_spacing / 2))
        
        for j in range(len(vertical_positions) + 1):
            x_center = int((j * horizontal_spacing) + (horizontal_spacing / 2))
            row.append((x_center, y_center))
        tile_centers.append(row)
    
    return grid, tile_centers

def display_grid(grid, tile_centers):
    plt.figure(figsize=(12, 8))
    plt.imshow(grid, cmap='binary')
    
    for row in tile_centers:
        for (x, y) in row:
            plt.plot(x, y, 'r.', markersize=5)
            
    plt.title('Grid Visualization (white = lines, black = empty, red dots = tile centers)')
    plt.axis('on')
    plt.grid(True, which='both', color='gray', linewidth=0.5, alpha=0.3)
    plt.show()
    
    print("\nGrid shape:", grid.shape)
    print(f"Number of tiles: {len(tile_centers) * len(tile_centers[0])}")

if __name__ == "__main__":
    grid, tile_centers = generate_jagged_grid("dog.jpg")
    display_grid(grid, tile_centers) 