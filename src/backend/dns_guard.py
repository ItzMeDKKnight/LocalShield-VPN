import asyncio
import httpx
from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, DNSHandler, BaseResolver

class DoHResolver(BaseResolver):
    def __init__(self, provider_url="https://1.1.1.1/dns-query"):
        self.provider_url = provider_url
        self.client = httpx.AsyncClient()

    async def resolve_doh(self, query_bytes):
        headers = {
            "Content-Type": "application/dns-message",
            "Accept": "application/dns-message"
        }
        response = await self.client.post(self.provider_url, content=query_bytes, headers=headers)
        if response.status_code == 200:
            return response.content
        return None

    def resolve(self, request, handler):
        # We need to run the async DoH call in a sync context for DNSServer
        query_bytes = request.pack()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response_bytes = loop.run_until_complete(self.resolve_doh(query_bytes))
            if response_bytes:
                return DNSRecord.parse(response_bytes)
        finally:
            loop.close()
        
        # Fallback to empty response
        reply = request.reply()
        return reply

class DNSGuard:
    def __init__(self, port=53, provider="cloudflare"):
        providers = {
            "cloudflare": "https://1.1.1.1/dns-query",
            "google": "https://dns.google/dns-query"
        }
        self.url = providers.get(provider, providers["cloudflare"])
        self.port = port
        self.server = None

    def start(self):
        resolver = DoHResolver(self.url)
        self.server = DNSServer(resolver, port=self.port, address="127.0.0.1")
        print(f"DNS Guard started on 127.0.0.1:{self.port} via {self.url}")
        self.server.start_thread()

    def stop(self):
        if self.server:
            self.server.stop()
            print("DNS Guard stopped.")

if __name__ == "__main__":
    # Test
    guard = DNSGuard()
    guard.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        guard.stop()
