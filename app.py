import base64
from flask import Flask, request, jsonify, render_template
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/homepage')
def index():
    return render_template('homepage.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json.get('data')

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create a QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format='PNG')
    img_bytes_io.seek(0)

    # Return the QR code image as a data URL
    img_data = img_bytes_io.read()
    img_base64 = base64.b64encode(img_data).decode()
    img_data_url = f'data:image/png;base64,{img_base64}'

    return img_data_url

if __name__ == '__main__':
    app.run(debug=True)
