import pytest
from unittest.mock import Mock, patch
from http_stream_xml.socket_stream import SocketStream
import socket
import ssl


def test_socket_stream_init():
    stream = SocketStream("example.com", "/test", ssl=True, port=443)
    assert stream.host == "example.com"
    assert stream.url == "/test"
    assert stream.port == 443
    assert stream.ssl == True
    assert stream.fetched_bytes == 0


def test_socket_stream_non_ssl():
    stream = SocketStream("example.com", "/test", ssl=False, port=80)
    assert isinstance(stream.socket, socket.socket)
    assert not isinstance(stream.socket, ssl.SSLSocket)


@patch("socket.socket")
@patch("ssl.create_default_context")
def test_socket_stream_connect_ssl(mock_ssl_context, mock_socket_class):
    # Create a mock socket instance with required attributes
    mock_socket_instance = Mock()
    mock_socket_instance.family = socket.AF_INET
    mock_socket_instance.type = socket.SOCK_STREAM
    mock_socket_instance.proto = 0
    mock_socket_instance.getsockopt.return_value = socket.SOCK_STREAM
    mock_socket_class.return_value = mock_socket_instance

    # Mock SSL context and wrapped socket
    mock_ssl_socket = Mock()
    mock_context = Mock()
    mock_context.wrap_socket.return_value = mock_ssl_socket
    mock_ssl_context.return_value = mock_context

    stream = SocketStream("example.com", "/test", ssl=True)
    stream.connect()

    # Verify SSL wrapping occurred
    mock_context.wrap_socket.assert_called_once_with(mock_socket_instance)
    # Verify connection was made with wrapped socket
    mock_ssl_socket.connect.assert_called_once_with(("example.com", 443))
    mock_ssl_socket.send.assert_called_once()


def test_socket_stream_empty_buffer():
    stream = SocketStream("example.com", "/test")
    stream.socket = Mock()
    stream.socket.recv.return_value = b""
    with pytest.raises(BufferError, match="Buffer is empty"):
        stream.read()
