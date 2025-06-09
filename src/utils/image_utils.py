from PIL import Image, ImageDraw, ImageFont, ImageOps
import discord
import io
import requests

def generate_default_welcome_image(member: discord.Member) -> discord.File:
    # Configuración de imagen
    width, height = 800, 400
    background_color = (30, 30, 30)
    avatar_size = 150
    username_font_size = 40

    # Crear imagen base
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Cargar avatar desde Discord
    avatar_url = member.display_avatar.replace(size=256, static_format="png").url
    response = requests.get(avatar_url)
    avatar_bytes = io.BytesIO(response.content)
    avatar = Image.open(avatar_bytes).convert("RGBA")
    avatar = avatar.resize((avatar_size, avatar_size))

    # Crear máscara circular
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    avatar.putalpha(mask)

    # Posición centrada del avatar
    avatar_x = (width - avatar_size) // 2
    avatar_y = 80
    image.paste(avatar, (avatar_x, avatar_y), avatar)

    # Texto (nombre del usuario)
    try:
        font = ImageFont.truetype("arial.ttf", username_font_size)
    except:
        font = ImageFont.load_default()

    username = member.display_name
    bbox = draw.textbbox((0, 0), username, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = avatar_y + avatar_size + 20

    draw.text((text_x, text_y), username, fill=(255, 255, 255), font=font)

    # Convertir a archivo de imagen
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return discord.File(fp=output, filename="welcome.png")
