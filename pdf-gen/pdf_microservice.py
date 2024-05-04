# app.py

from flask import Flask
import pdfmaker
import asyncio
app = Flask(__name__)

@app.route('/createpdf', methods=['GET'])
def createpdf():
    asyncio.run(pdfmaker.create_pdf_with_image_and_data("icon.png", "http://backend:8080/list", "output.pdf"))
    return "PDF created"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)