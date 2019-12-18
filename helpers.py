import socket


def communicate(host, port, request):
    """Facilitate communication between processes using sockets."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(request)
    response = sock.recv(1024)
    sock.close()
    return response
