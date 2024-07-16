import re
import argparse
import os

def parse_css_gradient(css_gradient):
    """
    Parse a linear CSS gradient with multiple color stops.
    Example input: "linear-gradient(to right, #fbb040, #fdb453, #ffb865, #ffbc76, #ffc186)"
    """
    pattern = r'linear-gradient\(([^,]+),\s*(.+)\)'
    match = re.match(pattern, css_gradient)
    if not match:
        raise ValueError("Invalid CSS gradient format")

    direction, colors_str = match.groups()
    if 'to right' not in direction:
        raise ValueError("Unsupported gradient direction")

    colors = colors_str.split(',')
    colors = [color.strip() for color in colors]

    return colors

def hex_to_rgb(hex_color):
    """
    Convert a hex color string to an RGB tuple.
    Example input: "#ff0000" -> output: (1.0, 0.0, 0.0)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def create_gimp_gradient(name, colors):
    """
    Create a GIMP gradient file content with multiple color stops.
    """
    num_segments = len(colors) - 1
    segments = []

    for i in range(num_segments):
        left_color = hex_to_rgb(colors[i])
        right_color = hex_to_rgb(colors[i+1])
        left_endpoint = i / num_segments
        right_endpoint = (i + 1) / num_segments
        midpoint = (left_endpoint + right_endpoint) / 2

        segment = [
            left_endpoint, midpoint, right_endpoint,
            *left_color, 1.0,
            *right_color, 1.0,
            0,  # Linear blending function
            0,  # RGB coloring type
            0,  # Fixed left endpoint color type
            0   # Fixed right endpoint color type
        ]
        segments.append(segment)

    gradient_content = [
        "GIMP Gradient",
        f"Name: {name}",
        str(num_segments)
    ]

    for segment in segments:
        gradient_content.append(" ".join(map(str, segment)))

    return "\n".join(gradient_content)

def write_gimp_gradient_file(content, file_path):
    """
    Write the gradient content to a .ggr file.
    """
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Convert a CSS gradient to a GIMP gradient.')
    parser.add_argument('css_gradient', type=str, help='The CSS gradient string (e.g., "linear-gradient(to right, #fbb040, #fdb453, #ffb865, #ffbc76, #ffc186)")')
    parser.add_argument('--name', type=str, default='Custom Gradient', help='The name of the GIMP gradient')
    parser.add_argument('--output', type=str, default='~/Library/Application Support/GIMP/2.10/gradients/', help='The output directory for the .ggr file')

    args = parser.parse_args()

    css_gradient = args.css_gradient
    gradient_name = args.name
    gimp_gradient_dir = os.path.expanduser(args.output)
    gimp_gradient_file = os.path.join(gimp_gradient_dir, f"{gradient_name}.ggr")

    colors = parse_css_gradient(css_gradient)
    gimp_gradient_content = create_gimp_gradient(gradient_name, colors)
    write_gimp_gradient_file(gimp_gradient_content, gimp_gradient_file)

    print(f"GIMP gradient saved to: {gimp_gradient_file}")

if __name__ == "__main__":
    main()
