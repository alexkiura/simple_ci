import argparse
import socketserver
import threading


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
    args = parser.parse_args()

    server = ThreadingTCPServer((args.host, int(args.port)), DispatcherHandler)
    print(f"Serving on {args.host}:{args.port}")
    runner_heartbeat = threading.Thread(target=runner_checker, args=(server,))
    redistributor = threading.Thread(target=redistribute, args=(server,))
    try:
        runner_heartbeat.start()
        redistributor.start()
        # Activate server to run indefinitely
        server.serve_forever()
    except (KeyboardInterrupt, Exception):
        # kill the thread if any exception occurs
        server.dead = True
        runner_heartbeat.join()
        redistributor.join()


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    runners = []  # tracks the test runner pool
    dead = False  # inform other threads that we're no longer running
    dispatched_commits = {}  # Keeps track of commits we have dispatched
    pending_commits = []  # track commits we're yet to dispatch
