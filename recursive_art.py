""" TODO: Put your header comment here """

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    var = ["x","y"]
    func = ["add","minus","times","sin","cos","square","cube","squareroot"]
    if max_depth == 1:
        return [var[random.randint(0,1)]]
    else:
        nfunc = func[random.randint(0,7)]
        if nfunc == "add" or "minus" or "times":
            return [nfunc,build_random_function(min_depth,max_depth-1),build_random_function(min_depth,max_depth-1)]
        else:
            return [nfunc,build_random_function(min_depth,max_depth-1)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if "x" in f[0]:
        return x
    elif "y" in f[0]:
        return y
    elif "add" in f[0]:
        return evaluate_random_function(f[1],x,y)+ evaluate_random_function(f[2],x,y)
    elif "minus" in f[0]:
        return evaluate_random_function(f[1],x,y)- evaluate_random_function(f[2],x,y)
    elif "times" in f[0]:
        return evaluate_random_function(f[1],x,y)* evaluate_random_function(f[2],x,y)
    elif "sin" in f[0]:
        return math.sin(evaluate_random_function(f[1],x,y))
    elif "cos" in f[0]:
        return math.cos(evaluate_random_function(f[1],x,y))
    elif "square" in f[0]:
        return evaluate_random_function(f[1],x,y)**2
    elif "squareroot" in f[0]:
        return evaluate_random_function(f[1],x,y)**(1/2)
    elif "cube" in f[0]:
        return evaluate_random_function(f[1],x,y)**3


def remap_interval(val,input_interval_start,input_interval_end,output_interval_start,output_interval_end):
    a = (val - input_interval_start + 0.0) / (input_interval_end - input_interval_start)
    b = a * (output_interval_end - output_interval_start) + output_interval_start
    return b




def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(0,7)
    green_function = build_random_function(0,8)
    blue_function = build_random_function(0,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function

    generate_art("example2.png")
    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
