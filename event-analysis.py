import requests
import json
import pandas as pd
from openpyxl import Workbook
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Faça uma requisição GET para o arquivo JSON no Azure Blob Storage
response = requests.get('https://placeholder.blob.core.windows.net/allevents/allevents/2024/10/27/events.all_1_.json')

# Split the response text by newlines to get a list of JSON strings
json_strings = response.text.split('\n')

# Initialize an empty list to store the JSON data
data = []

# Loop through the list of JSON strings
for json_str in json_strings:
    # Skip empty strings
    if json_str:
        # Convert each JSON string to a Python dictionary and append it to the list
        data.append(json.loads(json_str))

# Create a new workbook
wb = Workbook()

# Select the active worksheet
ws = wb.active

# Add headers to the worksheet
ws.append(['Timestamp', 'EventId', 'EventName', 'playFabBuildId', 'sessionId', 'matchResultTied', 'matchResultWinnerId', 'playerA', 'playerB'])

# Loop through the data and add each row to the worksheet
for event in data:
    timestamp = event['Timestamp']
    eventId = event['EventData'].get('EventId', '')
    eventName = event['EventData'].get('EventName', '')
    if 'GameAnalytics' in event['EventData']:
        playFabBuildId = event['EventData']['GameAnalytics'].get('playFabBuildId', '')
        sessionId = event['EventData']['GameAnalytics'].get('sessionId', '')
        matchResultTied = event['EventData']['GameAnalytics'].get('matchResultTied', '')
        matchResultWinnerId = event['EventData']['GameAnalytics'].get('matchResultWinnerId', '')
        playerA = json.dumps(event['EventData']['GameAnalytics'].get('playerA', ''), indent=4)
        playerB = json.dumps(event['EventData']['GameAnalytics'].get('playerB', ''), indent=4)
    else:
        playFabBuildId = ''
        sessionId = ''
        matchResultTied = ''
        matchResultWinnerId = ''
        playerA = ''
        playerB = ''
    ws.append([timestamp, eventId, eventName, playFabBuildId, sessionId, matchResultTied, matchResultWinnerId, playerA, playerB])


# Save the workbook to a file
wb.save('report.xlsx')

# Envie o gráfico por e-mail
msg = MIMEMultipart()
msg['From'] = 'placeholder@live.com'
msg['To'] = 'placeholder@live.com'
msg['Subject'] = 'Daily Report'

part = MIMEBase('application', 'octet-stream')
part.set_payload(open('report.xlsx', 'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="report.xlsx"')
msg.attach(part)

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login('placeholder@live.com', 'placeholderpass')
smtp.sendmail('placeholder@live.com', 'placeholder@live.com', msg.as_string())
smtp.quit()