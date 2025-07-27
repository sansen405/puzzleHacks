import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import deque
from generate_grid import generate_jagged_grid
import os

def bfs_tile(grid, start_point, height, width):
    tile_points = set()
    queue = deque([(start_point[0], start_point[1])])
    visited = np.zeros((height, width), dtype=bool)
    
    if grid[start_point[1], start_point[0]] == 1:
        found_start = False
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                new_x = start_point[0] + dx
                new_y = start_point[1] + dy
                if (0 <= new_x < width and 0 <= new_y < height and 
                    grid[new_y, new_x] == 0):
                    queue = deque([(new_x, new_y)])
                    found_start = True
                    break
            if found_start:
                break
        if not found_start:
            return tile_points

    visited[start_point[1], start_point[0]] = True
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    
    while queue:
        x, y = queue.popleft()
        if grid[y, x] == 0:
            tile_points.add((x, y))
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < width and 0 <= new_y < height and 
                not visited[new_y, new_x] and 
                grid[new_y, new_x] == 0):
                queue.append((new_x, new_y))
                visited[new_y, new_x] = True
    
    return tile_points

def debug_tile(grid, tile_points, center, filename):
    debug_img = np.zeros_like(grid)
    for x, y in tile_points:
        debug_img[y, x] = 1
    
    plt.figure(figsize=(10, 10))
    plt.imshow(debug_img, cmap='gray')
    plt.plot(center[0], center[1], 'r.', markersize=10)
    plt.title(f'Tile at center ({center[0]}, {center[1]})')
    plt.savefig(filename)
    plt.close()

def process_tiles(grid, tile_centers, original_image):
    width, height = original_image.size
    img_array = np.array(original_image)
    
    os.makedirs('tiles', exist_ok=True)
    num_rows = len(tile_centers)
    num_cols = len(tile_centers[0])
    tiles = [[None for _ in range(num_cols)] for _ in range(num_rows)]
    
    for i, row in enumerate(tile_centers):
        for j, (center_x, center_y) in enumerate(row):
            tile_points = bfs_tile(grid, (center_x, center_y), height, width)
            
            if not tile_points:
                print(f"Warning: No valid points found for tile {i}_{j}")
                continue
                
            mask = np.zeros((height, width), dtype=bool)
            for x, y in tile_points:
                mask[y, x] = True
            
            masked_img = img_array.copy()
            if len(masked_img.shape) == 3:
                masked_img[~mask] = 0
            else:
                masked_img[~mask] = 0
            
            if len(masked_img.shape) == 3:
                non_zero = np.where(masked_img.sum(axis=2) > 0)
            else:
                non_zero = np.where(masked_img > 0)
            
            if len(non_zero[0]) > 0 and len(non_zero[1]) > 0:
                y_min, y_max = non_zero[0].min(), non_zero[0].max()
                x_min, x_max = non_zero[1].min(), non_zero[1].max()
                
                #CROP
                cropped_img = masked_img[y_min:y_max+1, x_min:x_max+1]
                tiles[i][j] = cropped_img
                
                #SAVE
                tile_img = Image.fromarray(cropped_img)
                tile_filename = f'tiles/tile_{i}_{j}.jpg'
                tile_img.save(tile_filename, 'JPEG')
            else:
                print(f"Warning: Empty tile at position {i}_{j}")
    
    print(f"Saved tiles to 'tiles' directory")
    return tiles

def display_all_tiles(tiles):
    if not tiles:
        print("No valid tiles to display")
        return
    
    num_rows = len(tiles)
    num_cols = len(tiles[0])
    
    max_height = 0
    max_width = 0
    for row in tiles:
        for tile in row:
            if tile is not None:
                max_height = max(max_height, tile.shape[0])
                max_width = max(max_width, tile.shape[1])
    
    spacing = 20
    canvas_height = num_rows * (max_height + spacing) - spacing
    canvas_width = num_cols * (max_width + spacing) - spacing
    
    sample_tile = next(tile for row in tiles for tile in row if tile is not None)
    if len(sample_tile.shape) == 3:
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
    else:
        canvas = np.zeros((canvas_height, canvas_width), dtype=np.uint8)
    
    #PLACE_TILES
    for i in range(num_rows):
        for j in range(num_cols):
            tile = tiles[i][j]
            if tile is not None:
                y_start = i * (max_height + spacing)
                x_start = j * (max_width + spacing)
                
                y_offset = (max_height - tile.shape[0]) // 2
                x_offset = (max_width - tile.shape[1]) // 2
                
                if len(tile.shape) == 3:
                    canvas[y_start + y_offset:y_start + y_offset + tile.shape[0],
                          x_start + x_offset:x_start + x_offset + tile.shape[1]] = tile
                else:
                    canvas[y_start + y_offset:y_start + y_offset + tile.shape[0],
                          x_start + x_offset:x_start + x_offset + tile.shape[1]] = tile
    
    plt.figure(figsize=(20, 10))
    if len(sample_tile.shape) == 3:
        plt.imshow(canvas)
    else:
        plt.imshow(canvas, cmap='gray')
    plt.axis('off')
    plt.title('All Tiles (10x5 grid)')
    plt.show()

def display_grid_preview(grid, tile_centers):
    plt.figure(figsize=(12, 8))
    plt.imshow(grid, cmap='binary')
    for row in tile_centers:
        for (x, y) in row:
            plt.plot(x, y, 'r.', markersize=5)
    plt.title('Grid Preview')
    plt.axis('on')
    plt.show()

if __name__ == "__main__":
    grid, tile_centers = generate_jagged_grid("dog.jpg")
    original_image = Image.open("dog.jpg")
    tiles = process_tiles(grid, tile_centers, original_image)
    display_all_tiles(tiles)
    display_grid_preview(grid, tile_centers) 