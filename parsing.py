import base64
from googleapiclient.discovery import build
import re
from bs4 import BeautifulSoup
from summarizer import summarize_text
from reply import checkreply

def parse_emails(creds, timeframe = '1d', max_results = 3):
    """Fetches and parses emails within a given timeframe. It will return a list of emails
    with keys, subcet, sender, date, and body."""
    service = build('gmail', 'v1', credentials=creds)
    
    #Use gmail search query for time frame
    query = f'newer_than:{timeframe} category:primary'
    results = service.users().messages().list(userId = 'me', q = query, maxResults = max_results).execute()
    
    messages = results.get('messages', [])
    email_list = []
    Email_ID = 0
    
    for msg_meta in messages:
        msg_id = msg_meta['id']
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        payload = msg['payload']
        headers = payload.get('headers', [])

        subject = 'No Subject'
        sender = 'Unknown Sender'
        date = msg.get('internalDate', 'Unknown Date')
        #extracting subject and sender from header object
        for header in headers:
            if header['name'] == "Subject":
                subject = header['value']
            elif header['name'] == "From":
                sender = header['value']

        #Extractin the plain body text
        body = 'No Plain Text Body'
        body_plain = ""
        if 'parts' in payload:
            for parts in payload['parts']:
                if parts.get('mimeType') == 'text/html':
                    data = parts['body'].get('data')
                    decoded = base64.urlsafe_b64decode(data + '==').decode('utf-8')
                    body = decoded
                    body_plain = clean_html(decoded)
                    break
        # Fallback for body if not found in parts
        elif 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            decoded = base64.urlsafe_b64decode(data + '==').decode('utf-8')
            body = decoded

        # Summarize the plain text body (if it exists)
        summary = summarize_text(body_plain) if body_plain else "No summary available."
        #check whether a response is needed or not
        reply = checkreply(summary, subject, sender)

        email_list.append({
            'email ID'  : Email_ID,
            'subject'   : subject,
            'sender'    : sender,
            'date'      : date,
            'body'      : body,
            'body_plain': body_plain,
            'summary'   : summary,
            'reply'     : reply
        })
        Email_ID += 1
    
    return email_list

def clean_html(html):
    """Cleans the html content in the body for AI or search. Removing tags, scripts,
    styles, and white space"""
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip = True)
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with
    return text
