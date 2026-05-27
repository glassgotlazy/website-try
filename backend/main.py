from fastapi import FastAPI

app = FastAPI(title='MailMind AI')

@app.get('/')
def home():
    return {'message': 'MailMind AI Backend Running'}
