from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Define the server handler
class SimpleRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Read the incoming data

        try:
            # Attempt to parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            print(f"Received JSON data: {data}")

            # Save the data to a file
            with open("received_data.json", "a") as file:
                json.dump(data, file)
                file.write("\n")

            # Send a response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Data received"}).encode())

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Send a POST request with JSON data.")

# Server settings
def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8080):
    server_address = ('', port)  # Listen on all available interfaces
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

