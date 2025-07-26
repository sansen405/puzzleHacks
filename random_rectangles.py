from PIL import Image, ImageDraw
import random

def draw_jagged_lines(image_path):
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    width, height = img.size
    draw = ImageDraw.Draw(img)

    for i in range(9):
        center_x = (i + 1) * width // 10
        points = [(center_x, 0)]
        y = 0
        while y < height:
            y += random.randint(5, 10)
            x = center_x + random.randint(-5, 5)
            points.append((x, y))
        points.append((center_x + random.randint(-5, 5), height))
        draw.line(points, fill="red", width=2)

    for i in range(4):
        center_y = (i + 1) * height // 5
        points = [(0, center_y)]
        x = 0
        while x < width:
            x += random.randint(5, 10)
            y = center_y + random.randint(-5, 5)
            points.append((x, y))
        points.append((width, center_y + random.randint(-5, 5)))
        draw.line(points, fill="red", width=2)

    img.show()

def main():
    draw_jagged_lines("dog.jpg")

if __name__ == "__main__":
    main()
