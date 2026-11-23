"""
Launches the Student Records & Result Manager Dashboard in your default web browser.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    url = f"http://localhost:{PORT}/dashboard.html"
    print("=" * 70)
    print(" Starting Student Records & Result Manager Dashboard...")
    print(f" Serving at: {url}")
    print(" Press Ctrl+C in this terminal to stop the server.")
    print("=" * 70)

    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Note: Could not automatically open browser ({e}).")
        print(f"Please open your browser manually and visit: {url}")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    run()
