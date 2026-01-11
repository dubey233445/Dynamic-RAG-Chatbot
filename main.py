import time
import threading
from src.watcher import start_watcher
from src.bot import Chatbot

def main():
    # Start the file watcher in a separate thread/process setup
    # Watchdog runs in its own thread by default
    observer = start_watcher("./data")

    print("\nInitializing Chatbot...")
    bot = Chatbot()
    print("Chatbot ready! Type 'exit' to quit.")

    try:
        while True:
            query = input("\nYou: ")
            if query.lower() in ["exit", "quit"]:
                break
            
            response = bot.ask(query)
            print(f"Bot: {response}")

    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
