from urllib.request import urlopen

from main_react import start_api_server


def test_desktop_api_server_starts_on_available_port():
    server = start_api_server()
    try:
        with urlopen(f"http://127.0.0.1:{server.server_port}/api/stats", timeout=3) as response:
            assert response.status == 200
    finally:
        server.shutdown()
        server.server_close()
