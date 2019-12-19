import argparse


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
