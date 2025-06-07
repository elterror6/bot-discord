from PIL import Image,ImageDraw, ImageFont
import io
import discord

def generate_default_welcome_image():
    # Create a blank image with white background
    width, height = 800, 200
    image = Image.new("RGB", (width, height), color=(30,30,30))
    
    # Draw a welcome message
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    text = f"¡Bienvenido, {user}!"
    text_width, text_height = draw.textsize(text, font=font)
    
    # Calculate position for centered text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill=(255,255,255), font=font)
    
    with io.BytesIO() as image_io:
        image.save(image_io, format='PNG')
        image_io.seek(0)
        return discord.File(fp=image_io, filename='welcome_image.png')
    return image