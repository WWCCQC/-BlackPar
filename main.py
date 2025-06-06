from flask import Flask, jsonify, send_file   # เพิ่ม send_file
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    # ส่ง index.html ที่อยู่ใน root directory
    return send_file('index.html')

@app.route('/sheet-data')
def sheet_data():
    SERVICE_ACCOUNT_FILE = '/etc/secrets/service-account.json'
    SPREADSHEET_ID = '1zNBBwHesBSFBNejaH4uTGqD90I4snSMxTcxODSQdGiE'
    RANGE = 'Remain Par By Group Code!A1:U405'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        ranges=[RANGE],
        fields='sheets.data.rowData.values.formattedValue,sheets.data.rowData.values.effectiveFormat'
    ).execute()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
