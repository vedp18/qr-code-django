import os
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from .forms import QRCodeForm

from PIL import Image, ImageDraw, ImageFont

import qrcode


def generate_qr_code_view(request):
    
    if request.method == 'POST':
        form = QRCodeForm(request.POST)

        # validating form
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']

            img = qrcode.make(url)

            # creating QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_H, 
                box_size=10,
                border=4,
            )
            
            qr.add_data(url)
            qr.make(fit=True)


            # Create QR image
            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')


            # # --- Step 3: Add company name text in center ---
            # draw = ImageDraw.Draw(qr_img)
            # width, height = qr_img.size


            # # Choose font size relative to QR size
            # font_size = int(width / 10)
            # try:
            #     font = ImageFont.truetype("arial.ttf", font_size)
            # except:
            #     font = ImageFont.load_default()

            # # text_width, text_height = draw.textsize(res_name, font=font)
            # # ✅ NEW METHOD: use textbbox() instead of textsize()
            # bbox = draw.textbbox((0, 0), res_name, font=font)
            # text_width = bbox[2] - bbox[0]
            # text_height = bbox[3] - bbox[1]

            # # Background rectangle (white box behind text)
            # box_padding_x = 20
            # box_padding_y = 10
            # x0 = (width - text_width) // 2 - box_padding_x
            # y0 = (height - text_height) // 2 - box_padding_y
            # x1 = (width + text_width) // 2 + box_padding_x
            # y1 = (height + text_height) // 2 + box_padding_y + 20

            # draw.rectangle([x0, y0, x1, y1], fill="white")

            # # Write text (centered)
            # draw.text(((width - text_width) / 2, (height - text_height) / 2), res_name, fill="black", font=font)

            # # Add logo
            # logo = Image.open("logo.jpg")   # your logo image path
            # logo_size = 150

            # # Resize logo
            # logo.thumbnail((logo_size, logo_size))

            # # Get QR dimensions
            # qr_width, qr_height = qr_img.size
            # logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            # # Paste logo in center
            # qr_img.paste(logo, logo_pos, mask=logo if logo.mode == 'RGBA' else None)






            file_name = res_name.replace(" ", "_").lower() + '_menu.png'
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)    # media/<file_path>
            # img.save(file_path)

            # Save final QR
            qr_img.save(file_path)

            # QR Image URL
            qr_image_url = os.path.join(settings.MEDIA_URL, file_name) # for showing on html

            context = {
                'res_name': res_name,
                'file_name': file_name,
                'qr_image_url': qr_image_url
            }

            return render(request, 'qr_download_page.html', context=context)

    else:
        form = QRCodeForm()
        context = {
            'form': form
        }
        return render(request, 'generate_qr_code.html',context=context)
