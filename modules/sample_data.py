"""
Sample data, presets, and synthetic image generators for Food Verse AI.
Provides rich demonstration presets and sample images for 1-click testing.
"""

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

def create_sample_dish_image(dish_type: str = "salmon_bowl") -> Image.Image:
    """Generates an illustrative dish graphic for demonstration."""
    img = Image.new("RGB", (600, 450), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    if dish_type == "salmon_bowl":
        # Background plate / bowl
        draw.ellipse([80, 40, 520, 410], fill=(225, 231, 239), outline=(180, 190, 205), width=4)
        draw.ellipse([100, 60, 500, 390], fill=(255, 255, 255))
        # Quinoa base
        draw.ellipse([130, 90, 470, 360], fill=(245, 230, 202))
        # Grilled Salmon fillet
        draw.polygon([(220, 150), (380, 140), (410, 260), (250, 270)], fill=(249, 115, 22))
        # Grill marks
        for y_off in [170, 200, 230]:
            draw.line([(240, y_off), (390, y_off - 10)], fill=(154, 52, 18), width=3)
        # Avocado slices
        for i, angle in enumerate([290, 310, 330]):
            draw.chord([140 + i*15, 120 + i*25, 240 + i*15, 220 + i*25], 45, 225, fill=(132, 204, 22), outline=(101, 163, 13), width=2)
        # Edamame / Greens
        for coord in [(320, 290), (350, 310), (370, 280), (390, 305), (310, 330), (340, 340)]:
            draw.ellipse([coord[0], coord[1], coord[0]+22, coord[1]+22], fill=(34, 197, 94))
        # Sesame seeds
        for coord in [(270, 180), (290, 195), (320, 175), (340, 210), (360, 190)]:
            draw.ellipse([coord[0], coord[1], coord[0]+4, coord[1]+7], fill=(255, 255, 255))
        # Title banner
        draw.rectangle([0, 0, 600, 36], fill=(16, 185, 129))
        draw.text((20, 8), "SAMPLE MEAL: Mediterranean Wild Salmon & Quinoa Superfood Bowl", fill=(255, 255, 255))

    elif dish_type == "avocado_toast":
        draw.ellipse([60, 30, 540, 420], fill=(230, 235, 240), outline=(200, 210, 220), width=4)
        # Artisanal sourdough slice
        draw.rounded_rectangle([150, 120, 450, 330], radius=30, fill=(217, 160, 102), outline=(161, 98, 7), width=4)
        # Smashed avocado
        draw.rounded_rectangle([170, 140, 430, 310], radius=20, fill=(132, 204, 22))
        # Poached egg
        draw.ellipse([240, 180, 360, 280], fill=(255, 255, 255), outline=(229, 231, 235), width=2)
        draw.ellipse([275, 205, 325, 255], fill=(245, 158, 11))
        # Chili flakes and microgreens
        for coord in [(200, 160), (230, 220), (380, 190), (400, 250), (220, 280), (360, 280)]:
            draw.ellipse([coord[0], coord[1], coord[0]+6, coord[1]+6], fill=(225, 29, 72))
        draw.rectangle([0, 0, 600, 36], fill=(16, 185, 129))
        draw.text((20, 8), "SAMPLE MEAL: Sourdough Avocado Toast with Organic Poached Egg", fill=(255, 255, 255))

    elif dish_type == "paneer_tikka":
        draw.ellipse([60, 30, 540, 420], fill=(240, 230, 220), outline=(210, 190, 170), width=4)
        # Rice/Naan
        draw.ellipse([120, 80, 320, 260], fill=(254, 243, 199), outline=(217, 119, 6), width=2)
        # Curry bowl
        draw.ellipse([280, 150, 490, 360], fill=(220, 38, 38))
        # Paneer cubes
        for coord in [(320, 200), (370, 220), (340, 260), (410, 240), (380, 290)]:
            draw.rectangle([coord[0], coord[1], coord[0]+35, coord[1]+35], fill=(255, 255, 255), outline=(245, 158, 11), width=2)
        # Fresh coriander garnish
        for coord in [(350, 240), (370, 270), (400, 220)]:
            draw.ellipse([coord[0], coord[1], coord[0]+12, coord[1]+12], fill=(22, 101, 52))
        draw.rectangle([0, 0, 600, 36], fill=(16, 185, 129))
        draw.text((20, 8), "SAMPLE MEAL: Paneer Tikka Masala with Garlic Naan & Basmati", fill=(255, 255, 255))

    return img


def create_sample_produce_image(item_type: str = "fresh_apple") -> Image.Image:
    """Generates an illustrative produce item for freshness diagnostics."""
    img = Image.new("RGB", (600, 450), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    if item_type == "fresh_apple":
        # Apple body - vibrant red, glossy highlights
        draw.ellipse([170, 110, 430, 370], fill=(220, 38, 38))
        draw.ellipse([180, 110, 320, 360], fill=(239, 68, 68))
        # Stem & leaf
        draw.rectangle([292, 60, 308, 120], fill=(120, 53, 15))
        draw.ellipse([305, 70, 365, 105], fill=(34, 197, 94))
        # Gloss shine
        draw.arc([200, 140, 260, 220], start=180, end=270, fill=(255, 255, 255), width=6)
        draw.rectangle([0, 0, 600, 36], fill=(34, 197, 94))
        draw.text((20, 8), "SAMPLE PRODUCE: Grade A Fresh Crisp Honeycrisp Apple (Optimal Firmness)", fill=(255, 255, 255))

    elif item_type == "overripe_banana":
        # Banana body - yellow with heavy brown speckles and browning tips
        draw.arc([120, 100, 480, 380], start=30, end=170, fill=(234, 179, 8), width=55)
        # Stem tip
        draw.rectangle([130, 190, 160, 215], fill=(113, 63, 18))
        # Brown spots & senescence marks
        for coord in [(210, 280), (250, 310), (290, 320), (340, 310), (380, 280), (260, 295), (320, 325)]:
            draw.ellipse([coord[0], coord[1], coord[0]+14, coord[1]+10], fill=(120, 53, 15))
        draw.rectangle([0, 0, 600, 36], fill=(245, 158, 11))
        draw.text((20, 8), "SAMPLE PRODUCE: Overripe Banana (High Sugar, Peel Browning, Soft)", fill=(255, 255, 255))

    elif item_type == "spoiled_berries":
        # Strawberries with visible fuzzy gray mold colonies
        draw.polygon([(180, 180), (260, 340), (330, 190)], fill=(185, 28, 28))
        draw.polygon([(300, 160), (390, 320), (450, 170)], fill=(153, 27, 27))
        # Mold patches (Penicillium / Botrytis cinerea gray mycelium)
        draw.ellipse([210, 230, 280, 290], fill=(209, 213, 219), outline=(156, 163, 175), width=3)
        draw.ellipse([340, 210, 420, 280], fill=(156, 163, 175), outline=(107, 114, 128), width=3)
        # Calyx leaves (wilted)
        draw.polygon([(230, 180), (255, 150), (275, 180)], fill=(74, 90, 50))
        draw.rectangle([0, 0, 600, 36], fill=(225, 29, 72))
        draw.text((20, 8), "SAMPLE PRODUCE: Mold-Infested Strawberries (Botrytis cinerea Spores)", fill=(255, 255, 255))

    return img


def create_sample_kitchen_image(scene_type: str = "compliant") -> Image.Image:
    """Generates an illustrative commercial kitchen scene."""
    img = Image.new("RGB", (650, 450), color=(241, 245, 249))
    draw = ImageDraw.Draw(img)

    # Stainless steel counter
    draw.rectangle([0, 260, 650, 450], fill=(148, 163, 184))
    draw.line([0, 260, 650, 260], fill=(203, 213, 225), width=6)
    # Stainless backsplash / tile
    draw.rectangle([0, 36, 650, 260], fill=(226, 232, 240))
    for x in range(0, 650, 65):
        draw.line([x, 36, x, 260], fill=(203, 213, 225), width=2)
    for y in range(36, 260, 45):
        draw.line([0, y, 650, y], fill=(203, 213, 225), width=2)

    if scene_type == "compliant":
        # Sanitizer spray bottle labeled
        draw.rectangle([60, 200, 100, 280], fill=(59, 130, 246))
        draw.ellipse([65, 180, 95, 205], fill=(37, 99, 235))
        draw.text((63, 230), "SAN 200", fill=(255, 255, 255))

        # Green Cutting Board (Produce Only)
        draw.rounded_rectangle([150, 280, 370, 410], radius=8, fill=(34, 197, 94), outline=(22, 101, 52), width=3)
        draw.text((165, 290), "HACCP VEGETABLE STATION", fill=(255, 255, 255))
        # Chopped bell peppers
        draw.rectangle([200, 330, 230, 345], fill=(239, 68, 68))
        draw.rectangle([250, 350, 280, 365], fill=(234, 179, 8))

        # Chef representation (wearing hairnet & gloves)
        draw.ellipse([460, 80, 560, 180], fill=(254, 215, 170)) # Face
        draw.ellipse([450, 60, 570, 120], fill=(255, 255, 255), outline=(100, 116, 139), width=2) # Chef Hat / Hairnet
        draw.rectangle([430, 180, 590, 310], fill=(255, 255, 255), outline=(203, 213, 225), width=2) # White jacket
        # Blue nitrile gloves
        draw.ellipse([400, 290, 445, 330], fill=(14, 165, 233))
        draw.ellipse([570, 290, 615, 330], fill=(14, 165, 233))

        draw.rectangle([0, 0, 650, 36], fill=(16, 185, 129))
        draw.text((20, 8), "COMMERCIAL KITCHEN AUDIT: 100% Compliant HACCP Sanitized Station", fill=(255, 255, 255))

    elif scene_type == "hazard":
        # Violation 1: Raw chicken dripping near ready-to-eat salad on same wood board
        draw.rounded_rectangle([100, 280, 380, 420], radius=8, fill=(180, 130, 80), outline=(120, 80, 40), width=4)
        draw.text((110, 285), "POROUS WOOD (NON-COMPLIANT)", fill=(255, 255, 255))
        # Raw chicken cutlet
        draw.ellipse([130, 320, 230, 390], fill=(254, 205, 211), outline=(244, 63, 94), width=3)
        draw.text((140, 345), "RAW POULTRY", fill=(190, 18, 60))
        # Salad leaves touching chicken juices
        draw.ellipse([240, 320, 350, 400], fill=(132, 204, 22))
        draw.line([220, 360, 250, 360], fill=(244, 63, 94), width=4) # Cross-contact line

        # Violation 2: Worker with NO hairnet, NO gloves, uncovered bandage
        draw.ellipse([460, 80, 560, 180], fill=(254, 215, 170))
        # Exposed hair (no net)
        draw.arc([450, 60, 570, 140], 180, 360, fill=(69, 26, 3), width=18)
        draw.rectangle([430, 180, 590, 310], fill=(100, 116, 139)) # Street clothes, no apron
        # Bare hands touching food contact surface
        draw.ellipse([400, 290, 445, 330], fill=(254, 215, 170), outline=(225, 29, 72), width=3)

        # Violation 3: Cleaning chemical stored above open food prep
        draw.rectangle([520, 190, 570, 270], fill=(234, 179, 8))
        draw.text((525, 220), "BLEACH", fill=(0, 0, 0))

        draw.rectangle([0, 0, 650, 36], fill=(225, 29, 72))
        draw.text((20, 8), "CRITICAL HAZARD AUDIT: Raw Poultry Cross-Contamination & PPE Violations", fill=(255, 255, 255))

    return img


def image_to_base64_data_uri(pil_img: Image.Image) -> str:
    """Converts a PIL Image to a base64 data URI."""
    buf = BytesIO()
    pil_img.save(buf, format="PNG")
    b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"
