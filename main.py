from flask import Flask, jsonify, send_file
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# ---- แก้ไขตรงนี้ให้กรอกค่า SPREADSHEET_ID ----
SPREADSHEET_ID = "1zNBBwHesBSFBNejaH4uTGqD90I4snSMxTcxODSQdGiE" # <-- แก้ตรงนี้เป็นไฟล์ของคุณ
SERVICE_ACCOUNT_FILE = '/etc/secrets/service-account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

RANGES = [
    'Remain Par By Group Code!A1:U1000',
    'BlackByGroupCode!A1:U1000',
    'สรุปสถานะช่างอบรม!A1:Z1000',
    'กองงานช่าง!A1:Z1000'
]

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/sheet-data')
def sheet_data():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        ranges=RANGES,
        fields='sheets.properties.title,sheets.data.rowData.values.formattedValue,sheets.data.rowData.values.effectiveFormat'
    ).execute()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
