#!/usr/bin/env python3
"""
Download Bitcoin Icon
--------------------
This script downloads a Bitcoin icon for use with the application.
"""

import os
import requests
from PIL import Image
from io import BytesIO

def download_bitcoin_icon():
    """Download a Bitcoin icon and save it as an ICO file."""
    # Create docs directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    # URL for a Bitcoin icon (PNG format)
    icon_url = "https://cryptologos.cc/logos/bitcoin-btc-logo.png"
    
    try:
        # Download the image
        response = requests.get(icon_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        
        # Convert and save as ICO
        icon_path = os.path.join('docs', 'bitcoin.ico')
        image.save(icon_path, format='ICO', sizes=[(32, 32), (64, 64), (128, 128)])
        
        print(f"Bitcoin icon downloaded and saved to {icon_path}")
        return True
    except Exception as e:
        print(f"Error downloading Bitcoin icon: {str(e)}")
        
        # Create a simple colored square as a fallback
        try:
            # Create a simple orange square (Bitcoin color)
            image = Image.new('RGB', (128, 128), color=(242, 169, 0))
            
            # Add a 'B' in the center
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(image)
            try:
                # Try to use a system font
                font = ImageFont.truetype("arial.ttf", 80)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Draw the 'B' in white
            draw.text((40, 20), "₿", fill=(255, 255, 255), font=font)
            
            # Save as ICO
            icon_path = os.path.join('docs', 'bitcoin.ico')
            image.save(icon_path, format='ICO', sizes=[(32, 32), (64, 64), (128, 128)])
            
            print(f"Created fallback Bitcoin icon at {icon_path}")
            return True
        except Exception as e2:
            print(f"Error creating fallback icon: {str(e2)}")
            return False

if __name__ == "__main__":
    download_bitcoin_icon()
