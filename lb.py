import http.server
import http.client
import socketserver
import threading
import time


# List of backend server addresses and ports
backend_servers = [
    ("localhost", 5001)
    # Add more backend servers as needed
]

current_server = 0

class LoadBalancerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("----Serving request")
        global current_server
        # Get the next backend server in a round-robin fashion
        backend_server = backend_servers[current_server]
        #executing_server = current_server
        current_server = (current_server + 1) % len(backend_servers)
        #print("----Selected server--->"+ current_server)

        try:
            # Create a connection to the backend server
            print("-------Creating Connection--------------")
            conn = http.client.HTTPConnection(backend_server[0], backend_server[1])
            print("--------Creating Request-------------")
            #print(self.path, "---#---", self.rfile);
            start_time = time.time()
            conn.request("GET", self.path, headers=dict(self.headers))
            print("-------Getting Response--------------")
            response = conn.getresponse()
            end_time = time.time()
            et = end_time-start_time
            print(et)
            print("-------Got Response--------------")
            # Send the backend server's response back to the client
            self.send_response(response.status)
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.read())
        except Exception as e:
            # Handle exceptions (e.g., if a backend server is down)
            self.send_error(500, str(e))
class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass
if __name__ == '__main__':
    # Start the load balancer server
    server_address = ('localhost', 8080)
    httpd = ThreadingHTTPServer(server_address, LoadBalancerHandler)
    print('Load balancer listening on port 8080...')
    httpd.serve_forever()
