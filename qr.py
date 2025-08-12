import qrcode
from PIL import Image, ImageDraw
import urllib.parse

# WhatsApp URL format: https://wa.me/<number>?text=<urlencoded_text>
# Example:
phone_number = "1111111111111"  # Use country code, no + or dashes
message = "Hello, this is a test message!"
encoded_message = urllib.parse.quote(message)
url = f"https://wa.me/{phone_number}?text={encoded_message}"

# Create QR code with higher error correction to allow for logo overlay
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(url)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# Open the WhatsApp logo
try:
    logo = Image.open("wpp.png")
    if logo.mode in ("P", "PA"):
        logo = logo.convert("RGBA")

    # Calculate the size for the logo (10% of QR)
    qr_width, qr_height = qr_img.size
    logo_size = min(qr_width, qr_height) // 5
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_bg = Image.new("RGB", (logo_size + 20, logo_size + 20), "white")
    if logo.mode == "RGBA":
        white_bg = Image.new("RGB", logo.size, "white")
        white_bg.paste(logo, mask=logo.split()[-1])
        logo = white_bg
    logo_bg.paste(logo, (10, 10))
    logo_pos = ((qr_width - logo_bg.width) // 2, (qr_height - logo_bg.height) // 2)
    qr_img.paste(logo_bg, logo_pos)

    print("QR code with WhatsApp logo created successfully!")

except FileNotFoundError:
    print("Warning: wpp.png not found. Creating QR code without logo.")
except Exception as e:
    print(f"Error processing logo: {e}. Creating QR code without logo.")

qr_img.save("whatsapp_qr_with_logo.png")
print("QR code saved as 'whatsapp_qr_with_logo.png'")
