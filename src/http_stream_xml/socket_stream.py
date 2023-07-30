import socket
import ssl

HEADER = "GET {url} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {agent}\r\nContent-Type: application/x-www-form-urlencoded; charset=UTF-8\r\nContent-Length: 0"
END_OF_REQUEST = (
    b"\r\n\r\n\r\n\r\n"  # two times CR/LF + empty body + 2 times CR/LF to complete the request
)
END_OF_LINE = "\r\n"
BEGIN_OF_BODY = "\r\n\r\n"


class SocketStream:
    """Simple socket stream reader."""

    def __init__(self, host, url, ssl=True, port=443):
        """Init."""
        self.host = host
        self.url = url
        self.agent = "For the lulz.."
        self.ssl = ssl
        self.port = port

        self.socket = self.get_socket()
        self.fetched_bytes = 0

    def get_socket(self):
        """Get socket object."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return ssl.create_default_context().wrap_socket(sock) if self.ssl else sock

    @property
    def header(self):
        """Get HTTP header."""
        return HEADER.format(host=self.host, url=self.url, agent=self.agent).encode()

    def connect(self):
        """Connect to host and send header."""
        self.socket.connect((self.host, self.port))
        self.socket.send(self.header + END_OF_REQUEST)

    def close(self):
        """Close socket."""
        self.socket.close()

    def read(self, bufsize=1024):
        """Read from socket."""
        buf = self.socket.recv(bufsize)
        if not buf:
            raise BufferError
        self.fetched_bytes += len(buf)
        return buf.decode()

    def is_chunk_head_line(self, line):
        """Check if line is chunk head line."""
        return 0 < len(line) < 5 and line[0] in "0123456789abcdef"

    def fetch(self, bufsize=1024):
        """Fetch data from socket."""
        chunk = ""
        while True:
            chunk += self.read(bufsize)
            body_start = chunk.find(BEGIN_OF_BODY)
            if body_start >= 0:
                chunk = chunk[chunk.find(BEGIN_OF_BODY) + len(BEGIN_OF_BODY) :]
                break
        while True:
            result = []
            for line in chunk.split(END_OF_LINE)[:-1]:  # skip uncomplete line
                if self.is_chunk_head_line(line):
                    continue
                result.append(line)
            result = END_OF_LINE.join(result)
            yield result
            chunk = chunk.split("\r\n")[-1]  # start collecting with uncomplete line
            chunk += self.read(bufsize)
