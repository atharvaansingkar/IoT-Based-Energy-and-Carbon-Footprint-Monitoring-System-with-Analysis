import webview
from threading import Thread
from app import app  # Ensure your Flask app is imported correctly

def start_flask_app():
    app.run()

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    Thread(target=start_flask_app).start()

    # Start the PyWebView window
    webview.create_window('Vision App', 'http://127.0.0.1:5000')
    webview.start()
