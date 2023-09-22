from io import BytesIO
import qrcode
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


@app.route('/qr', methods=['GET', 'POST'])
def generate_qr_code():
    # Get the URL from the query parameter 'url'
    if request.method == "POST":
        url = request.json.get('url')
        if url:
            qr_img = qrcode.make(url)

        else:
            return jsonify({'error': 'Missing URL parameter'}), 400
    else:
        url = request.args.get('url')
        if url:
            qr_img = qrcode.make(url)
        else:
            return jsonify({'error': 'Missing URL parameter'}), 400

    # Generate the QR code for the short URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to bytes
    img_buffer = BytesIO()
    qr_img.save(img_buffer)
    img_bytes = img_buffer.getvalue()

    # Return the QR code image and short URL as a response

    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': 'attachment; filename="qr.png"',
    }

    # Return the QR code image as a response

    return Response(img_bytes, 200, headers=headers)


if __name__ == '__main__':
    app.run(debug=False)
