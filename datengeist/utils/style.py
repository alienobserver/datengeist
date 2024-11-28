import colorsys

import cv2 as cv
import streamlit as st
from PIL import Image

def set_logo(path_to_logo: str):
    """
    Displays a logo image in the Streamlit app from the given path.

    Parameters:
    - path_to_logo (str): The file path to the logo image.

    Returns:
    - None
    """
    # Load the image using OpenCV
    logo = cv.imread(path_to_logo)

    # Check if the image was loaded successfully
    if logo is None:
        st.error("Image not found. Please check the file path.")
    else:
        # Convert BGR to RGB as OpenCV loads images in BGR format
        logo_rgb = cv.cvtColor(logo, cv.COLOR_BGR2RGB)

        # Convert NumPy array to PIL Image for Streamlit compatibility
        logo_pil = Image.fromarray(logo_rgb)

        # Display the image in Streamlit with large size
        st.logo(logo_pil, size='large')

def add_top_margin_div(size: int):
    """
    Adds a top margin to the Streamlit layout by injecting a div with a specified margin size.

    Parameters:
    - size (int): The top margin size in pixels.
    """
    top_margin = f"""
                <div style="height: {size}px;">
                </div>
                """

    st.markdown(top_margin, unsafe_allow_html=True)

def set_st_padding(size: int):
    """
    Sets padding for the entire Streamlit main container.

    Parameters:
    - size (int): The padding size in pixels to apply around the main container.
    """
    hide_streamlit_style = f"""
                <style>
                    .stMainBlockContainer {{padding: {size}px;}}
                </style>
                """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def set_st_hz_block(position: str):
    """
    Adjusts the alignment of items within a horizontal block container in Streamlit.

    Parameters:
    - position (str): The vertical alignment of the items (e.g., 'center', 'flex-start', 'flex-end').
    """
    # Change the main container layout
    center_items = f"""
                <style>
                    .stHorizontalBlock {{height: calc(100vh - 250px); align-items: {position};}}
                </style>
                """

    st.markdown(center_items, unsafe_allow_html=True)

def set_page_link_button_style():
    """
    Customizes the style of the page link buttons in Streamlit with a specific background color
    and hover effect.
    """
    page_link_button_style = """
                <style>
                    .stPageLink a {
                        background-color: #FF3232;
                    }
                    .stPageLink a:hover {
                        background-color: #BD2929;
                    }
                </style>
                """

    st.markdown(page_link_button_style, unsafe_allow_html=True)

"© Vahram"
class ColorGenerator:
    def __init__(self, saturation: float = 0.65, lightness: float = 0.60):
        """
        Initialize the color generator with specific saturation and lightness values.

        Args:
            saturation (float): Color saturation value between 0 and 1 (default: 0.65)
            lightness (float): Color lightness value between 0 and 1 (default: 0.60)
        """

        self.saturation = saturation
        self.lightness = lightness

    def generate_colors(self, n_colors: int):
        """
        Generate n_colors distinct RGB colors.

        Args:
            n_colors (int): Number of colors to generate

        Returns:
            List of RGB tuples, where each value is between 0 and 255
        """
        colors = []
        hue = 0

        for _ in range(n_colors):
            hue += 0.8 / n_colors

            # Convert HSL to RGB
            rgb = colorsys.hls_to_rgb(hue, self.lightness, self.saturation)

            # Convert to 8-bit RGB values
            rgb_int = tuple(int(255 * x) for x in rgb)
            colors.append(rgb_int)

        return colors

    def generate_hex_colors(self, n_colors: int):
        """
        Generate n_colors distinct colors in hex format.

        Args:
            n_colors (int): Number of colors to generate

        Returns:
            List of hex color strings (e.g., '#FF0000' for red)
        """
        rgb_colors = self.generate_colors(n_colors)

        return [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in rgb_colors]