from scrapybara import Scrapybara
from scrapybara.anthropic import Anthropic
from scrapybara.tools import BashTool, ComputerTool, EditTool
from scrapybara.prompts import UBUNTU_SYSTEM_PROMPT
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
import time
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

load_dotenv()

def initialize_firebase():
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if not firebase_admin._apps:  
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def get_next_command(last_timestamp):
    db = firestore.client()
    commands_ref = db.collection('commands')
    
    if isinstance(last_timestamp, (int, float)):
        last_timestamp = datetime.datetime.fromtimestamp(last_timestamp)
    
    query = (commands_ref
             .where('timestamp', '>', last_timestamp)
             .order_by('timestamp')
             .limit(1))
    
    docs = list(query.stream())
    print(f"Querying for new commands...")
    
    if docs:
        data = docs[0].to_dict()
        new_timestamp = data.get('timestamp')
        if new_timestamp:
            return data.get('command'), new_timestamp
    
    return None, last_timestamp

def main():
    initialize_firebase()
    client = Scrapybara(api_key=os.getenv("SCRAPYBARA_API_KEY"))
    instance = client.start_ubuntu(timeout_hours=0.5)
    print("Ubuntu instance started at:", instance.get_stream_url().stream_url)
    time.sleep(10) 

    last_timestamp = datetime.datetime(1970, 1, 1)

    try:
        while True:
            command, new_timestamp = get_next_command(last_timestamp)
            if command is None:
                print("No new command detected. Waiting...")
            else:
                print(f"Detected command: {command}")
                
                response = client.act(
                    model=Anthropic(),
                    tools=[BashTool(instance), ComputerTool(instance), EditTool(instance)],
                    system=UBUNTU_SYSTEM_PROMPT,
                    prompt=command,
                    on_step=lambda step: print(step.text)
                )
                print("Command completed, waiting for further commands...")
                last_timestamp = new_timestamp
            
            time.sleep(10)
    finally:
        instance.stop()
        print("Ubuntu instance stopped.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")