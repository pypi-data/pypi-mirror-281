import matplotlib.pyplot as plt


def generate_hex_colors(n: int) -> list:
    """
    Generate a list of unique hexadecimal colors.

    Parameters:
    n : int
        The number of colors to generate.

    Returns:
    list
        A list of unique hexadecimal colors.
    """
    # Get a list of default colors from the current color cycle
    default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # If n is greater than the number of default colors, generate additional colors
    if n > len(default_colors):
        num_colors_needed = n - len(default_colors)
        additional_colors = [
            "#%02x%02x%02x" % (r, g, b)
            for r in range(0, 256, num_colors_needed)
            for g in range(0, 256, num_colors_needed)
            for b in range(0, 256, num_colors_needed)
        ]
        colors = default_colors + additional_colors
    else:
        colors = default_colors[:n]

    return colors
