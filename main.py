"""



import torch
canvas_height = 1000
canvas_width = 1500

#loop to show different values
for i in range(5):
    #create normal distribution to sample from
    start_y_dist = torch.distributions.Normal(canvas_height * 0.8, canvas_height * 0.05)
    #sample from distribution
    start_y = int(start_y_dist.sample())

    #create normal distribution to sample height from
    height_dist = torch.distributions.Normal(canvas_height * 0.2, canvas_height * 0.05)

    height = int(height_dist.sample())
    end_y = start_y + height

    #start_x is fixed because of this being centered
    start_x = canvas_width // 2
    width_dist = torch.distributions.Normal(height * 0.5, height * 0.1)

    width = int(width_dist.sample())
    end_x = start_x + width

    print(f"start_x: {start_x}, end_x: {end_x}, start_y: {start_y}, end_y: {end_y}, width: {width}, height: {height}")


from PIL import Image, ImageDraw

# Create a new image with white background

# Loop to draw rectangles
for i in range(5):
    img = Image.new('RGB', (canvas_width, canvas_height), 'white')

    draw = ImageDraw.Draw(img)

    # Creating normal distributions to sample from
    start_y_dist = torch.distributions.Normal(canvas_height * 0.8, canvas_height * 0.05)
    start_y = int(start_y_dist.sample())

    height_dist = torch.distributions.Normal(canvas_height * 0.2, canvas_height * 0.05)
    height = int(height_dist.sample())
    end_y = start_y + height

    start_x = canvas_width // 2
    width_dist = torch.distributions.Normal(height * 0.5, height * 0.1)
    width = int(width_dist.sample())
    end_x = start_x + width

    # Drawing the rectangle
    draw.rectangle([(start_x, start_y), (end_x, end_y)], outline='black')

    img.show()



import torch
from PIL import Image, ImageDraw

# Setting the size of the canvas
canvas_size = 1000
# Number of lines
num_lines = 10
# Create distributions for start and end y-coordinates and x-coordinate
y_start_distribution = torch.distributions.Normal(canvas_size / 2, canvas_size / 4)
y_end_distribution = torch.distributions.Normal(canvas_size / 2, canvas_size / 4)
x_distribution = torch.distributions.Normal(canvas_size / 2, canvas_size / 4)
# Sample from the distributions for each line
y_start_points = y_start_distribution.sample((num_lines,))
y_end_points = y_end_distribution.sample((num_lines,))
x_points = x_distribution.sample((num_lines,))
# Create a white canvas
image = Image.new('RGB', (canvas_size, canvas_size), 'white')
draw = ImageDraw.Draw(image)
# Draw the lines
for i in range(num_lines):
    draw.line([(x_points[i], y_start_points[i]), (x_points[i], y_end_points[i])], fill='black')
# Display the image
image.show()
"""
from PIL import Image, ImageDraw
import numpy as np
import torch
# Define your line length
L = 3000

# Calculate the desired mean for the half-normal distribution
mu = np.sqrt(L * 2)

# Calculate the scale parameter that gives the desired mean
scale = mu / np.sqrt(2 / np.pi)

# Create a half-normal distribution with the calculated scale parameter
dist = torch.distributions.HalfNormal(scale / 3)

# Sample and draw multiple circles
    # Create a new image with white background
img_size = (2000, 2000)
img = Image.new('RGB', img_size, (255, 255, 255))
draw = ImageDraw.Draw(img)
for _ in range(10):


    # Define the center of the circles
    start_x = img_size[0] // 2
    start_y = img_size[1] // 2
    # Sample a radius from the distribution
    r = int(dist.sample())

    print(f"Sampled radius: {r}")

    # Define the bounding box for the circle
    bbox = [start_x - r, start_y - r, start_x + r, start_y + r]

    # Draw the circle onto the image
    draw.ellipse(bbox, outline ='black',fill=(0, 0, 0))

    # Display the image
    #img.show()
img.save("circles.png")