import http.server
import http.client

# List of backend server addresses and ports
backend_servers = [
    ("localhost", 5001),
    ("localhost", 5002),
    ("localhost", 7217),
    # Add more backend servers as needed
]

current_server = 0

class LoadBalancerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global current_server
        # Get the next backend server in a round-robin fashion
        backend_server = backend_servers[current_server]
        current_server = (current_server + 1) % len(backend_servers)

        try:
            # Create a connection to the backend server
            conn = http.client.HTTPConnection(backend_server[0], backend_server[1])
            conn.request("GET", self.path, headers=dict(self.headers))
            response = conn.getresponse()

            # Send the backend server's response back to the client
            print("-----Respons returned from remote server")
            self.send_response(response.status)
            print("-----Responding from load balancer")
            res = response.read()
            print(res)
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write("Success")
        except Exception as e:
            # Handle exceptions (e.g., if a backend server is down)
            self.send_error(500, str(e))

if __name__ == '__main__':
    # Start the load balancer server
    server_address = ('localhost', 8080)
    httpd = http.server.HTTPServer(server_address, LoadBalancerHandler)
    print('Load balancer listening on port 8080...')
    httpd.serve_forever()
