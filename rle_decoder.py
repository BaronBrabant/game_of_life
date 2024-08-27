import numpy as np

def decode_rle_file(file_path):
    with open(file_path, 'r') as file:
        rle_lines = parse_rle(file.read())
        header_line = rle_lines[0]
        x, y = parse_header(header_line)
        rle_data = ''.join(rle_lines[1:])
        grid = decode_rle(rle_data, x, y)
        return grid, x, y

def parse_rle(rle_string):
    """Parses the RLE encoded string and returns a list of lines."""
    lines = rle_string.strip().splitlines()
    # Remove any comment lines
    rle_lines = [line for line in lines if not line.startswith('#')]
    print(rle_lines)
    return rle_lines

def parse_header(header_line):
    """Parses the header to extract the grid dimensions."""
    header_parts = header_line.split(',')
    x = int(header_parts[0].split('=')[1])
    y = int(header_parts[1].split('=')[1])
    return x, y

def decode_rle(rle_data, width, height):
    """Decodes the RLE data into a numpy array of shape (height, width)."""
    grid = np.zeros((height, width), dtype=int)
    x = 0
    y = 0
    
    count = 0
    for char in rle_data:
        if char.isdigit():
            count = count * 10 + int(char)
        elif char == 'b':
            count = max(count, 1)
            x += count
            count = 0
        elif char == 'o':
            count = max(count, 1)
            grid[y, x:x+count] = 1
            x += count
            count = 0
        elif char == '$':
            y += max(count, 1)
            x = 0
            count = 0
        elif char == '!':
            break
    
    return grid


