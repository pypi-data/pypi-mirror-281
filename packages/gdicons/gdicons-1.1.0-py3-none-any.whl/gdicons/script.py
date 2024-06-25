import os
import math
from PIL import Image, ImageOps, ImageEnhance
from PIL.Image import Resampling
from .plist import split_spritesheet, get_animdesc

RESOURCES_FOLDER = ""
ICONS_FOLDER = ""
ROBOT_ANIMDESC = {}
SPIDER_ANIMDESC = {}

def set_resources_path(resources_path):
    global RESOURCES_FOLDER, ICONS_FOLDER, ROBOT_ANIMDESC, SPIDER_ANIMDESC

    RESOURCES_FOLDER = resources_path
    ICONS_FOLDER = os.path.join(RESOURCES_FOLDER, "icons")

    robot_animdesc_path = os.path.join(RESOURCES_FOLDER, "Robot_AnimDesc.plist")
    spider_animdesc_path = os.path.join(RESOURCES_FOLDER, "Spider_AnimDesc.plist")

    if os.path.exists(robot_animdesc_path):
        ROBOT_ANIMDESC = get_animdesc(robot_animdesc_path, "Robot_idle")
    else:
        raise FileNotFoundError(f"Robot animdesc not found at {robot_animdesc_path}")

    if os.path.exists(spider_animdesc_path):
        SPIDER_ANIMDESC = get_animdesc(spider_animdesc_path, "Spider_idle")
    else:
        raise FileNotFoundError(f"Spider animdesc not found at {spider_animdesc_path}")

set_resources_path(r"C:\Program Files (x86)\Steam\steamapps\common\Geometry Dash\Resources")

COORDINATE_MULTIPLIERS = {
    "":    1,
    "hd":  2,
    "uhd": 4
}

ROBOT_PARTS = {
    1: "head",
    2: "connector",
    3: "leg",
    4: "foot"
}

SPIDER_PARTS = {
    1: "head",
    2: "leg",
    3: "back leg",
    4: "connector"
}

PLAYER_FORMS = {
    "cube":    "player",
    "ship":    "ship",
    "ball":    "player_ball",
    "ufo":     "bird",
    "wave":    "dart",
    "robot":   "robot",
    "spider":  "spider",
    "swing":   "swing",
    "jetpack": "jetpack"
}

# Return filepath to the spritesheet and .plist file associated
# with a
def get_filepaths(player_form, id, quality):
    player_form = PLAYER_FORMS[player_form]
    id = str(id).rjust(2, "0")
    quality = quality if not quality else f"-{quality}"

    filename = f"{player_form}_{id}{quality}"

    return (os.path.join(ICONS_FOLDER, f"{filename}.png"),
            os.path.join(ICONS_FOLDER, f"{filename}.plist"))

# Reorders a sprite dictionary based on what layer each texture
# should be on
def sort_layers(sprites):
    glow_layers = []
    dome_layers = []
    secondary_layers = []
    primary_layers = []
    extra_layers = []

    for sprite_name in sprites:
        if "glow" in sprite_name:
            glow_layers.append(sprite_name)

        elif "_3_" in sprite_name:
            dome_layers.append(sprite_name)

        elif "_2_" in sprite_name:
            secondary_layers.append(sprite_name)

        elif "extra" in sprite_name:
            extra_layers.append(sprite_name)

        else:
            primary_layers.append(sprite_name)

    ordered_sprite_names = (
        glow_layers + dome_layers + secondary_layers + primary_layers + extra_layers
    )

    return dict(zip(
        ordered_sprite_names,
        (sprites[sprite_name] for sprite_name in ordered_sprite_names)
    ))

def colorize_sprites(sprites, color_1, color_2, glow):
    colorized_sprites = sprites.copy()

    for sprite_name, sprite_data in sprites.items():
        image = sprite_data["image"]
        color = None

        if "glow" in sprite_name:
            if not glow:
                del colorized_sprites[sprite_name]
            else:
                color = glow

        elif "_2_" in sprite_name:
            color = color_2

        elif "extra" not in sprite_name and "_3_" not in sprite_name:
            color = color_1

        if color:
            colorized_sprites[sprite_name]["image"] = colorize_image(image, color)

    return colorized_sprites

def colorize_image(image, color):
    alpha = image.split()[-1]
    grayscale = ImageOps.grayscale(image)
    result = ImageOps.colorize(grayscale, (0, 0, 0, 0), color)
    result.putalpha(alpha)

    return result

# A factor of 0.0 = black
def darken_image(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Combines layers into a single image, including their offsets
def combine_layers(sprites):
    combined = Image.new("RGBA", (400, 200))

    for _, sprite_data in sprites.items():
        image = sprite_data["image"]
        offset = sprite_data["offset"]

        layer_x = 200 - image.width // 2 + round(offset[0])
        layer_y = 100 - image.height // 2 - round(offset[1])

        combined.alpha_composite(image, (layer_x, layer_y))

    return combined.crop(combined.getbbox())

# Convert a robot's sprite dictionary to a tuple of layers
# to be combined later
def split_robot_parts(sprites):
    head_sprites = {}
    connector_sprites = {}
    leg_sprites = {}
    foot_sprites = {}

    head_glow_texture = None
    connector_glow_texture = None
    leg_glow_texture = None
    foot_glow_texture = None

    for sprite_name, sprite_data in sprites.items():
        part_id = int(sprite_name.split("_")[2])
        part = ROBOT_PARTS[part_id]
        entry = {sprite_name: sprite_data}

        if "glow" in sprite_name:
            image = sprite_data["image"]

            if part == "head": head_glow_texture = image
            elif part == "connector": connector_glow_texture = image
            elif part == "leg": leg_glow_texture = image
            elif part == "foot": foot_glow_texture = image

        elif part == "head": head_sprites.update(entry)
        elif part == "connector": connector_sprites.update(entry)
        elif part == "leg": leg_sprites.update(entry)
        elif part == "foot": foot_sprites.update(entry)

    parts = {
        "head": combine_layers(head_sprites),
        "connector": combine_layers(connector_sprites),
        "leg": combine_layers(leg_sprites),
        "foot": combine_layers(foot_sprites)
    }

    # Store glow textures separately so they are all layered behind
    # the body sprites
    return (
        (darken_image(parts["leg"], 0.7), leg_glow_texture),
        (darken_image(parts["connector"], 0.7), connector_glow_texture),
        (darken_image(parts["foot"], 0.7), foot_glow_texture),
        (parts["head"], head_glow_texture),
        (parts["leg"].copy(), leg_glow_texture.copy()),
        (parts["connector"].copy(), connector_glow_texture.copy()),
        (parts["foot"].copy(), foot_glow_texture.copy())
    )

def split_spider_parts(sprites):
    head_sprites = {}
    leg_sprites = {}
    back_leg_sprites = {}
    connector_sprites = {}

    head_glow_texture = None
    leg_glow_texture = None
    back_leg_glow_texture = None
    connector_glow_texture = None

    for sprite_name, sprite_data in sprites.items():
        part_id = int(sprite_name.split("_")[2])
        part = SPIDER_PARTS[part_id]
        entry = {sprite_name: sprite_data}

        if "glow" in sprite_name:
            image = sprite_data["image"]

            if part == "head": head_glow_texture = image
            elif part == "leg": leg_glow_texture = image
            elif part == "back leg": back_leg_glow_texture = image
            elif part == "connector": connector_glow_texture = image

        elif part == "head": head_sprites.update(entry)
        elif part == "leg": leg_sprites.update(entry)
        elif part == "back leg": back_leg_sprites.update(entry)
        elif part == "connector": connector_sprites.update(entry)

    parts = {
        "head": combine_layers(head_sprites),
        "leg": combine_layers(leg_sprites),
        "back leg": combine_layers(back_leg_sprites),
        "connector": combine_layers(connector_sprites)
    }

    return (
        (darken_image(parts["leg"], 0.5), leg_glow_texture),
        (darken_image(parts["leg"].copy(), 0.5), leg_glow_texture.copy()),
        (parts["connector"], connector_glow_texture),
        (parts["head"], head_glow_texture),
        (parts["back leg"].copy(), back_leg_glow_texture.copy()),
        (parts["leg"].copy(), leg_glow_texture.copy()),
    )

# Applies necessary animdesc transformations and returns
# as a new sprite dictionary
def sprites_from_animdesc(icon_parts, animdesc, coord_multiplier):
    glow_sprites = {}
    part_sprites = {}

    for part, part_data in animdesc.items():
        part_texture, glow_texture = icon_parts[part]

        position = part_data["position"]
        position = [round(coord * coord_multiplier) for coord in position]
        rotation = part_data["rotation"]
        scale = part_data["scale"]
        flipped_x, flipped_y = part_data["flipped"]

        # Resize textures
        part_texture = part_texture.resize((
            round(part_texture.width * scale[0]),
            round(part_texture.height * scale[1])
        ))
        glow_texture = glow_texture.resize((
            round(glow_texture.width * scale[0]),
            round(glow_texture.height * scale[1])
        ))
        # Mirror images horizontally/vertically
        if flipped_x:
            part_texture = ImageOps.mirror(part_texture)
            glow_texture = ImageOps.mirror(glow_texture)
        if flipped_y:
            part_texture = ImageOps.flip(part_texture)
            glow_texture = ImageOps.flip(glow_texture)
        # Rotate textures
        part_texture = part_texture.rotate(-rotation, resample=Resampling.BICUBIC, expand=True)
        glow_texture = glow_texture.rotate(-rotation, resample=Resampling.BICUBIC, expand=True)

        glow_sprites.update({
            part: {
                "image": glow_texture, "offset": position
            }
        })
        part_sprites.update({
            part + len(animdesc): {
                "image": part_texture, "offset": position
            }
        })

    return {**glow_sprites, **part_sprites}

# The function you actually use
def render_icon(
    gamemode: str,
    id: int,
    primary: str,
    secondary: str,
    glow: str | bool = False,
    quality: str = "uhd"
):
    quality = "" if quality not in ["hd", "uhd"] else quality
    coord_multiplier = COORDINATE_MULTIPLIERS[quality]

    sprites = split_spritesheet(*get_filepaths(gamemode, id, quality))
    sprites = sort_layers(sprites)
    sprites = colorize_sprites(sprites, primary, secondary, glow)

    if gamemode == "robot":
        robot_parts = split_robot_parts(sprites)
        sprites = sprites_from_animdesc(robot_parts, ROBOT_ANIMDESC, coord_multiplier)

    elif gamemode == "spider":
        spider_parts = split_spider_parts(sprites)
        sprites = sprites_from_animdesc(spider_parts, SPIDER_ANIMDESC, coord_multiplier)

    return combine_layers(sprites)
