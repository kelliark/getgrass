import asyncio
import random
import ssl
import json
import time
import uuid
import base64
import aiohttp
from datetime import datetime
from colorama import init, Fore, Style
from websockets_proxy import Proxy, proxy_connect

init(autoreset=True)

BANNER = """
   _____        _             __    
  / ___/ _____ (_)____   ____/ /____
  \\__ \\ / ___// // __ \\ / __  // __ \\
 ___/ // /__ / // / / // /_/ // /_/ /
/____/ \\___//_//_/ /_/ \\__,_/ \\____/
"""

EDGE_USERAGENTS = [
    # Microsoft Edge (Latest)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.57",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.46",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.128",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.112",
    
    # Chrome (Latest)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    # Firefox (Latest)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.0; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    
    # Safari (Latest)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    
    # Microsoft Edge (Mobile)
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 EdgA/121.0.2277.112",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36 EdgA/121.0.2277.112",
    
    # Chrome (Mobile)
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.66 Mobile/15E148 Safari/604.1",
    
    # Firefox (Mobile)
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/121.0 Firefox/121.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/121.0 Firefox/121.0",
    
    # Edge (Older versions)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.133",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.121",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91",
    
    # Chrome (Older versions)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    
    # Firefox (Older versions)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0"
]

HTTP_STATUS_CODES = {
    200: "OK",
    201: "Created", 
    202: "Accepted",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden", 
    404: "Not Found",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

class ProxyManager:
    def __init__(self):
        self.proxy_file = "proxy.txt"
        self.error_proxy_file = "error-proxy.txt"
        self.used_proxies = set()
        self.failed_proxies = set()
        self.proxy_lock = asyncio.Lock()
    
    async def load_proxies(self):
        try:
            with open(self.proxy_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}Error: {self.proxy_file} not found{Style.RESET_ALL}")
            return []
    
    async def mark_proxy_as_failed(self, proxy):
        async with self.proxy_lock:
            if proxy not in self.failed_proxies:
                self.failed_proxies.add(proxy)
                # Add to error-proxy.txt
                with open(self.error_proxy_file, 'a') as f:
                    f.write(f"{proxy}\n")
                
                # Remove from proxy.txt
                try:
                    with open(self.proxy_file, 'r') as f:
                        proxies = f.readlines()
                    
                    with open(self.proxy_file, 'w') as f:
                        for p in proxies:
                            if p.strip() != proxy:
                                f.write(p)
                                
                    print(f"{Fore.RED}Moved failing proxy to {self.error_proxy_file}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error updating proxy files: {str(e)}{Style.RESET_ALL}")
    
    async def get_new_proxy(self, user_id):
        async with self.proxy_lock:
            all_proxies = await self.load_proxies()
            available_proxies = [p for p in all_proxies if p not in self.used_proxies and p not in self.failed_proxies]
            
            if not available_proxies:
                print(f"{Fore.RED}No more available proxies!{Style.RESET_ALL}")
                return None
            
            new_proxy = random.choice(available_proxies)
            self.used_proxies.add(new_proxy)
            print(f"{Fore.GREEN}Assigned new proxy for user {user_id}{Style.RESET_ALL}")
            return new_proxy

proxy_manager = ProxyManager()

def format_log(message, proxy=None, device_id=None, action=None, data=None, color=Fore.WHITE):
    """Format log message in a clean and beautiful way"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    proxy_short = proxy.split("@")[-1].split(":")[0][-8:] if proxy else "direct"
    device_short = device_id[-8:] if device_id else "unknown"
    
    # Format the log parts
    parts = []
    parts.append(f"{Fore.BLUE}[{timestamp}]{Style.RESET_ALL}")
    parts.append(f"{Fore.CYAN}[{proxy_short}]{Style.RESET_ALL}")
    parts.append(f"{Fore.YELLOW}[{device_short}]{Style.RESET_ALL}")
    
    if action:
        parts.append(f"{color}[{action}]{Style.RESET_ALL}")
    
    parts.append(message)
    
    if data:
        # Format JSON data in a cleaner way
        if isinstance(data, dict):
            data_str = f"id: {data.get('id', 'N/A')}"
            if 'action' in data:
                data_str += f", action: {data['action']}"
            parts.append(f"{Fore.GREEN}{data_str}{Style.RESET_ALL}")
    
    return " ".join(parts)

async def connect_to_wss(socks5_proxy, user_id, mode):
    retry_count = 0
    max_retries = 3  # Maximum number of proxy retries per connection
    
    while retry_count < max_retries:
        try:
            device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, socks5_proxy))
            
            random_user_agent = random.choice(EDGE_USERAGENTS)
            
            print(format_log("INITIALIZATION", socks5_proxy, device_id, "INITIALIZATION", {"user_agent": random_user_agent}, Fore.MAGENTA))
            
            has_received_action = False
            is_authenticated = False
            
            while True:
                try:
                    await asyncio.sleep(random.randint(1, 10) / 10)
                    custom_headers = {
                        "User-Agent": random_user_agent,
                        "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi" if mode == "extension" else None
                    }
                    custom_headers = {k: v for k, v in custom_headers.items() if v is not None}
                    
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    
                    urilist = [
                        #"wss://proxy.wynd.network:4444/",
                        #"wss://proxy.wynd.network:4650/",
                        "wss://proxy2.wynd.network:4444/",
                        "wss://proxy2.wynd.network:4650/",
                        #"wss://proxy3.wynd.network:4444/",
                        #"wss://proxy3.wynd.network:4650/"
                    ]
                    uri = random.choice(urilist)
                    server_hostname = "proxy.wynd.network"
                    proxy = Proxy.from_url(socks5_proxy)
                    
                    async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                             extra_headers=custom_headers) as websocket:
                        async def send_ping():
                            while True:
                                if has_received_action:
                                    send_message = json.dumps(
                                        {"id": str(uuid.uuid5(uuid.NAMESPACE_DNS, socks5_proxy)), 
                                         "version": "1.0.0", 
                                         "action": "PING", 
                                         "data": {}})
                                    
                                    print(format_log("SENDING PING", socks5_proxy, device_id, "PING", send_message, Fore.MAGENTA))
                                    
                                    await websocket.send(send_message)
                                    await websocket.ping()
                                await asyncio.sleep(5)

                        await asyncio.sleep(1)
                        ping_task = asyncio.create_task(send_ping())

                        while True:
                            if is_authenticated and not has_received_action:
                                print(format_log("AUTHENTICATED | WAIT UNTIL THE PING GATE OPENS", socks5_proxy, device_id, "AUTHENTICATED", {"message": "Waiting for " + ("HTTP_REQUEST" if mode == "extension" else "OPEN_TUNNEL")}, Fore.MAGENTA))
                            
                            response = await websocket.recv()
                            message = json.loads(response)
                            
                            print(format_log("RECEIVED", socks5_proxy, device_id, "RECEIVED", message, Fore.CYAN))

                            if message.get("action") == "AUTH":
                                auth_response = {
                                    "id": message["id"],
                                    "origin_action": "AUTH",
                                    "result": {
                                        "browser_id": device_id,
                                        "user_id": user_id,
                                        "user_agent": random_user_agent,
                                        "timestamp": int(time.time()),
                                        "device_type": "extension" if mode == "extension" else "desktop",
                                        "version": "4.26.2" if mode == "extension" else "4.30.0"
                                    }
                                }
                                
                                if mode == "extension":
                                    auth_response["result"]["extension_id"] = "lkbnfiajjmbhnfledhphioinpickokdi"
                                
                                print(format_log("AUTHENTICATING", socks5_proxy, device_id, "AUTH", auth_response, Fore.MAGENTA))
                                
                                await websocket.send(json.dumps(auth_response))
                                is_authenticated = True
                            
                            elif message.get("action") in ["HTTP_REQUEST", "OPEN_TUNNEL"]:
                                has_received_action = True
                                request_data = message["data"]
                                
                                headers = {
                                    "User-Agent": custom_headers["User-Agent"],
                                    "Content-Type": "application/json; charset=utf-8"
                                }
                                
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(request_data["url"], headers=headers) as api_response:
                                        content = await api_response.text()
                                        encoded_body = base64.b64encode(content.encode()).decode()
                                        
                                        status_text = HTTP_STATUS_CODES.get(api_response.status, "")
                                        
                                        http_response = {
                                            "id": message["id"],
                                            "origin_action": message["action"],
                                            "result": {
                                                "url": request_data["url"],
                                                "status": api_response.status,
                                                "status_text": status_text,
                                                "headers": dict(api_response.headers),
                                                "body": encoded_body
                                            }
                                        }
                                        
                                        print(format_log("OPENING PING ACCESS", socks5_proxy, device_id, "OPENING PING ACCESS", http_response, Fore.MAGENTA))
                                        
                                        await websocket.send(json.dumps(http_response))

                            elif message.get("action") == "PONG":
                                pong_response = {"id": message["id"], "origin_action": "PONG"}
                                
                                print(format_log("RECEIVED PONG", socks5_proxy, device_id, "PONG", pong_response, Fore.GREEN))
                                
                                await websocket.send(json.dumps(pong_response))
                                
                except Exception as e:
                    error_msg = str(e)
                    print(format_log(f"Error: {error_msg}", socks5_proxy, device_id, "ERROR", None, Fore.RED))
                    
                    # Check if it's a connection error (HTTP 500 or connection refused)
                    if "500" in error_msg or "rejected" in error_msg or "refused" in error_msg:
                        await proxy_manager.mark_proxy_as_failed(socks5_proxy)
                        
                        # Try to get a new proxy
                        new_proxy = await proxy_manager.get_new_proxy(user_id)
                        if new_proxy:
                            socks5_proxy = new_proxy
                            retry_count += 1
                            continue
                        else:
                            print(format_log(f"No more proxies available for user {user_id}", None, None, "ERROR", None, Fore.RED))
                            break
                    
                    await asyncio.sleep(5)
                    
        except Exception as e:
            error_msg = str(e)
            print(format_log(f"Error: {error_msg}", socks5_proxy, None, "ERROR", None, Fore.RED))
            
            # Check if it's a connection error (HTTP 500 or connection refused)
            if "500" in error_msg or "rejected" in error_msg or "refused" in error_msg:
                await proxy_manager.mark_proxy_as_failed(socks5_proxy)
                
                # Try to get a new proxy
                new_proxy = await proxy_manager.get_new_proxy(user_id)
                if new_proxy:
                    socks5_proxy = new_proxy
                    retry_count += 1
                    continue
                else:
                    print(format_log(f"No more proxies available for user {user_id}", None, None, "ERROR", None, Fore.RED))
                    break
            
            await asyncio.sleep(5)
            
    return None

async def main():
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Kelliark | GetGrass Farmer V2 - Multi Account{Style.RESET_ALL}")
    
    global proxy_manager
    proxy_manager = ProxyManager()
    
    print(f"{Fore.GREEN}Select Mode:{Style.RESET_ALL}")
    print("1. Extension Mode - Recommended")
    print("2. Desktop Mode - Unavailable")
    
    while True:
        mode_choice = input("Enter your choice (1/2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
    
    mode = "extension" if mode_choice == "1" else "desktop"
    print(f"{Fore.GREEN}Selected mode: {mode}{Style.RESET_ALL}")
    
    # Read user IDs from uid.txt
    try:
        with open('uid.txt', 'r') as file:
            user_ids = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: uid.txt not found. Please create it with one user ID per line.{Style.RESET_ALL}")
        return
    
    if not user_ids:
        print(f"{Fore.RED}Error: No user IDs found in uid.txt{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Found {len(user_ids)} accounts in uid.txt{Style.RESET_ALL}")
    
    # Read proxies
    try:
        with open('proxy.txt', 'r') as file:
            all_proxies = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: proxy.txt not found{Style.RESET_ALL}")
        return
    
    if not all_proxies:
        print(f"{Fore.RED}Error: No proxies found in proxy.txt{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Total available proxies: {len(all_proxies)}{Style.RESET_ALL}")
    
    while True:
        try:
            proxies_per_account = int(input(f'Enter number of proxies per account (max {len(all_proxies) // len(user_ids)}): '))
            if proxies_per_account <= 0:
                print(f"{Fore.RED}Please enter a positive number{Style.RESET_ALL}")
                continue
            if proxies_per_account * len(user_ids) > len(all_proxies):
                print(f"{Fore.RED}Not enough proxies. Maximum allowed: {len(all_proxies) // len(user_ids)} per account{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
    
    # Distribute proxies among accounts
    tasks = []
    proxy_index = 0
    
    for user_id in user_ids:
        # Get proxies for this account
        account_proxies = all_proxies[proxy_index:proxy_index + proxies_per_account]
        proxy_index += proxies_per_account
        
        print(f"{Fore.GREEN}Starting {proxies_per_account} instances for account: {user_id}{Style.RESET_ALL}")
        
        # Create tasks for this account
        account_tasks = [asyncio.ensure_future(connect_to_wss(proxy, user_id, mode)) 
                        for proxy in account_proxies]
        tasks.extend(account_tasks)
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
