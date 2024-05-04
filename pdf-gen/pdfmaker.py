from PyPDF2 import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import json
from datetime import datetime
import requests
from telegram import Bot
import asyncio

def get_json_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve JSON data from the URL.", flush=True)
        return None

async def fetch_item_info(item_id):
    url = f"http://backend:8080/warehouse?item_id={item_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve item info for item_id: {item_id}")
        return None

async def send_pdf_to_telegram(bot_token, chat_id, output_path):
    bot = Bot(token=bot_token)
    await bot.send_document(chat_id=chat_id, document=open(output_path, 'rb'))

async def create_pdf_with_image_and_data(image_path, data_url, output_path):
    # Read data from URL
    data = get_json_from_url(data_url)
    if not data:
        print("No data retrieved from the URL.")
        return

    # Create a canvas to draw on
    c = canvas.Canvas(output_path, pagesize=letter)

    # Draw the image onto the canvas with black background treated as transparent
    c.drawImage(image_path, 20, 740, width=100, height=50, mask='auto')

    # Add the title "INVOICE" centered between the icon and the text
    title = "INVOICE"
    title_width = c.stringWidth(title)  # Get the width of the title
    middle_point = (250 + title_width / 2 + 25)  # Calculate the middle point
    c.setFont("Helvetica-Bold", 16)  # Set font size and type for the title
    c.drawString(middle_point - title_width / 2, 750, title)  # Draw the title

    # Add the date to the top-right corner
    today = datetime.today().strftime("%Y-%m-%d")
    c.setFont("Helvetica", 12)  # Reset font size and type for the other text
    c.drawString(500, 770, "Date: " + today)

    # Add the NIF number below the date
    c.drawString(500, 750, "NIF N2434524")

    # Define data for the table
    table_data = [['ID', 'Name', 'Quantity', 'Price/u']]  # Table header
    total_income = 0

    for entry in data:
        item_id = entry['item_id']
        print(f"Fetching item info for item_id: {item_id}")
        item_info = await fetch_item_info(item_id)
        if item_info:
            name = item_info[0]['product']['name']
            price_per_unit = item_info[0]['product']['price']
            quantity = entry['quantity']
            total_income += price_per_unit * quantity
            table_data.append([entry['item_id'], name, quantity, f"{price_per_unit} /u"])

    # Add the total income row
    c.setFont("Helvetica-Bold", 14)
    table_data.append(['', '', '', f'Total: {total_income}€'])

    # Create a table and style
    table = Table(table_data, colWidths=[50, 200, 100, 100])
    style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                        ('GRID', (0, 0), (-1, -2), 1, colors.black)])

    table.setStyle(style)

    # Calculate the position of the table
    table_width, table_height = table.wrap(0, 0)
    table_x = (letter[0] - table_width) / 2
    table_y = (letter[1] - table_height - 100)  # Position below everything and in the middle

    # Add the table to the canvas
    table.drawOn(c, table_x, table_y)

    # Save the canvas to a PDF
    c.save()

    # Send the PDF to Telegram
    bot_token = '6881230062:AAFzu2_v9gVMmx0r4gap9ErO9MTvjU9D4bo'
    chat_id = '-4205309923'  # ID of the Telegram group
    await send_pdf_to_telegram(bot_token, chat_id, output_path)

if __name__ == "__main__":
    asyncio.run(create_pdf_with_image_and_data("icon.png", "http://backend:8080/list", "output.pdf"))
