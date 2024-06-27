class ProxyFormatter:
    @staticmethod
    def format_for_requests(proxy, delimiter=":"):
        print("format_proxy.py--proxy var ", proxy)
        """Formats the proxy for use with the Requests library."""
        parts = proxy.split(delimiter)
        if len(parts) == 2:
            return {
                "http": f"http://{parts[0]}:{parts[1]}",
                "https": f"https://{parts[0]}:{parts[1]}"
            }
        elif len(parts) == 4:
            return {
                "http": f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}",
                "https": f"https://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            }
        else:
            raise ValueError("Invalid proxy format")

    @staticmethod
    def format_for_selenium(proxy, delimiter=":"):
        """Formats the proxy for use with Selenium, including optional authentication."""
        parts = proxy.split(delimiter)
        print("format_proxy.py delimiter var", delimiter)
        print("format_proxy.py parts list total", len(parts))
        print("format_proxy.py proxy var", proxy)
        print("format_proxy.py parts var, split delimiter", parts)
        if len(parts) == 2:
            return {
                "proxyType": "MANUAL",
                "httpProxy": f"{parts[0]}:{parts[1]}",
                "sslProxy": f"{parts[0]}:{parts[1]}"
            }
        elif len(parts) == 4:
            return {
                "proxyType": "MANUAL",
                "httpProxy": f"{parts[0]}:{parts[1]}",
                "sslProxy": f"{parts[0]}:{parts[1]}",
                "socksUsername": parts[2],
                "socksPassword": parts[3]
            }
        else:
            raise ValueError("Invalid proxy format")

