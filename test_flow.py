import os
import time
import shutil
from src.watcher import start_watcher
from src.bot import Chatbot

def test_dynamic_update():
    # Setup
    data_dir = "./data"
    test_file = os.path.join(data_dir, "test_secret.txt")
    
    # Ensure clean state
    if os.path.exists(test_file):
        os.remove(test_file)
        
    print("Starting watcher...")
    observer = start_watcher(data_dir)
    
    try:
        # Initial check
        bot = Chatbot()
        # Create a test file
        print("Creating new document...")
        with open(test_file, "w") as f:
            f.write("The secret code for the verification test is ALPHA-ZULU-99.")
            
        print("Waiting for ingestion (5s)...")
        time.sleep(5)
        
        # Query
        print("Querying chatbot...")
        # We need to reload the vectorstore or ensure it sees updates. 
        # Chroma usually handles updates well, but let's re-instantiate bot to be safe/sure 
        # or just rely on the existing connection if it supports dynamic reads.
        # For simplicity, let's re-create bot to get fresh retriever
        bot = Chatbot() 
        results = bot.retriever.invoke("What is the secret code?")
        
        found = False
        for doc in results:
            if "ALPHA-ZULU-99" in doc.page_content:
                found = True
                break
        
        if found:
            print("SUCCESS: Secret code found in vector DB!")
        else:
            print("FAILURE: Secret code NOT found.")
            print("Docs found:", [d.page_content for d in results])
            
    finally:
        observer.stop()
        observer.join()
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_dynamic_update()
