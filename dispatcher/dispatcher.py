import argparse
import socketserver


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",
                        help="dispatcher's host (default is localhost)",
                        default="localhost",
                        action="store")
    parser.add_argument("--port",
                        help="dispatcher's port (default is 8888)",
                        default=8888,
                        action="store")
    agrs = parser.parse_args()


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    runners = []  # tracks the test runner pool
    dead = False  # inform other threads that we're no longer running
    dispatched_commits = {}  # Keeps track of commits we have dispatched
    pending_commits = []  # track commits we're yet to dispatch
