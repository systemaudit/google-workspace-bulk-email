#!/usr/bin/env python3
"""
Google Workspace Bulk Email Creator
Professional tool for automated user account creation in Google Workspace
"""

import os
import sys
import json
import random
import time
import platform
import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'
DOMAIN_FILE = 'domain.txt'
PASSWORD_FILE = 'password.txt'
NAME_FILE = 'nama.txt'
PORT = 8080
RATE_LIMIT_DELAY = 0.5  # Delay between API calls

class GoogleWorkspaceManager:
    """Main class for managing Google Workspace operations"""
    
    def __init__(self):
        self.service = None
        self.environment = self._detect_environment()
        self.domain = None
        self.password = None
        self.first_names = []
        self.last_names = []
        
    def _detect_environment(self) -> str:
        """Detect if running in VPS or local environment"""
        if os.environ.get('SSH_CLIENT') or os.environ.get('SSH_TTY'):
            return 'vps'
        if os.environ.get('DISPLAY') or platform.system() == 'Windows':
            return 'local'
        if os.path.exists('/.dockerenv') or os.path.exists('/proc/vz'):
            return 'vps'
        return 'vps'
    
    def display_header(self):
        """Display application header"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 60)
        print("GOOGLE WORKSPACE BULK EMAIL CREATOR")
        print(f"Environment: {self.environment.upper()}")
        print("=" * 60)
        print()
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed"""
        required_packages = {
            'google-auth': 'google.auth',
            'google-auth-oauthlib': 'google_auth_oauthlib',
            'google-auth-httplib2': 'google.auth.transport',
            'google-api-python-client': 'googleapiclient',
            'requests': 'requests'
        }
        
        missing_packages = []
        for package, module in required_packages.items():
            try:
                __import__(module)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error("Missing required packages: %s", ', '.join(missing_packages))
            print(f"\nPlease install missing packages:")
            print(f"pip install {' '.join(missing_packages)}\n")
            return False
        
        return True
    
    def create_default_files(self):
        """Create default configuration files if they don't exist"""
        # Create domain.txt
        if not os.path.exists(DOMAIN_FILE):
            domain = input("Enter Google Workspace domain (e.g., company.com): ").strip()
            if not domain:
                domain = "example.com"
                logger.warning("No domain provided, using default: %s", domain)
            
            with open(DOMAIN_FILE, 'w') as f:
                f.write(domain)
            logger.info("Created %s", DOMAIN_FILE)
        
        # Create nama.txt with default Indonesian names
        if not os.path.exists(NAME_FILE):
            default_names = """# Name database for email generation
# Format: DEPAN (first names) or BELAKANG (last names) followed by names

DEPAN Andi Budi Citra Dewi Eko Fitri Galih Hani Indra Joko Kartika Lestari Maya Novi Oki Putri Rina Sari Tari Umar Vina Wulan Yuni Zaki Agus Bayu Candra Dian Erna Fajar Gita Hendra Ika Jihan
BELAKANG Pratama Sari Putra Dewi Santoso Lestari Wijaya Rahayu Setiawan Wati Kusuma Anggraini Nugroho Safitri Permana Maharani Saputra Puspita Handoko Fitriani
"""
            with open(NAME_FILE, 'w') as f:
                f.write(default_names)
            logger.info("Created %s with default names", NAME_FILE)
        
        # Create password.txt
        if not os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, 'w') as f:
                f.write("Email123@")
            logger.info("Created %s with default password", PASSWORD_FILE)
    
    def load_configuration(self) -> bool:
        """Load configuration from files"""
        try:
            # Load domain
            if os.path.exists(DOMAIN_FILE):
                with open(DOMAIN_FILE, 'r') as f:
                    self.domain = f.read().strip() or "example.com"
            else:
                self.domain = "example.com"
            
            # Load password
            if os.path.exists(PASSWORD_FILE):
                with open(PASSWORD_FILE, 'r') as f:
                    self.password = f.read().strip() or "Email123@"
            else:
                self.password = "Email123@"
            
            # Load names
            self.first_names = []
            self.last_names = []
            
            if os.path.exists(NAME_FILE):
                with open(NAME_FILE, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split()
                            if len(parts) > 1:
                                if parts[0].upper() == 'DEPAN':
                                    self.first_names.extend(parts[1:])
                                elif parts[0].upper() == 'BELAKANG':
                                    self.last_names.extend(parts[1:])
            
            # Use defaults if empty
            if not self.first_names:
                self.first_names = ['User', 'Admin', 'Test']
            if not self.last_names:
                self.last_names = ['One', 'Two', 'Three']
            
            logger.info("Configuration loaded successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to load configuration: %s", e)
            return False
    
    def setup_oauth(self) -> bool:
        """Setup OAuth2 authentication"""
        if self.environment == 'vps':
            return self._setup_oauth_vps()
        else:
            return self._setup_oauth_local()
    
    def _setup_oauth_vps(self) -> bool:
        """OAuth2 setup for VPS environment (manual flow)"""
        import requests
        from urllib.parse import urlencode, urlparse, parse_qs
        import secrets
        
        logger.info("Starting OAuth2 setup for VPS environment")
        
        # Setup credentials
        if not self._setup_credentials():
            return False
        
        # Load credentials
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_data = json.load(f)
        
        client_info = creds_data.get('web', creds_data.get('installed'))
        
        # Generate authorization URL
        state = secrets.token_urlsafe(32)
        auth_params = {
            'response_type': 'code',
            'client_id': client_info['client_id'],
            'redirect_uri': 'http://localhost:8080',
            'scope': ' '.join(SCOPES),
            'state': state,
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        auth_url = f"{client_info['auth_uri']}?{urlencode(auth_params)}"
        
        print("\n" + "=" * 60)
        print("OAUTH2 AUTHORIZATION REQUIRED")
        print("=" * 60)
        print("\n1. Open this URL in your browser:")
        print(f"\n{auth_url}\n")
        print("2. Login with Google Workspace administrator account")
        print("3. Click 'Allow' to grant permissions")
        print("4. Copy the complete redirect URL from browser")
        print("\nExample: http://localhost:8080/?state=...&code=...&scope=...")
        print("-" * 60)
        
        redirect_url = input("\nPaste redirect URL here: ").strip()
        
        if not redirect_url:
            logger.error("No redirect URL provided")
            return False
        
        # Extract authorization code
        try:
            parsed = urlparse(redirect_url)
            params = parse_qs(parsed.query)
            
            if 'code' not in params:
                logger.error("Authorization code not found in URL")
                return False
            
            auth_code = params['code'][0]
            logger.info("Authorization code extracted successfully")
            
        except Exception as e:
            logger.error("Failed to parse redirect URL: %s", e)
            return False
        
        # Exchange code for token
        return self._exchange_code_for_token(client_info, auth_code)
    
    def _setup_oauth_local(self) -> bool:
        """OAuth2 setup for local environment (browser flow)"""
        import webbrowser
        import threading
        import http.server
        import socketserver
        from urllib.parse import urlencode, urlparse, parse_qs
        import secrets
        
        logger.info("Starting OAuth2 setup for local environment")
        
        # Setup credentials
        if not self._setup_credentials():
            return False
        
        # OAuth handler
        auth_code = None
        
        class OAuthHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                nonlocal auth_code
                
                parsed_path = urlparse(self.path)
                query_params = parse_qs(parsed_path.query)
                
                if 'code' in query_params:
                    auth_code = query_params['code'][0]
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    html = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Authorization Successful</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                            .success { color: #4CAF50; }
                        </style>
                    </head>
                    <body>
                        <h1 class="success">Authorization Successful</h1>
                        <p>You can close this window and return to the application.</p>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode())
                else:
                    self.send_response(400)
                    self.end_headers()
            
            def log_message(self, format, *args):
                pass  # Suppress logs
        
        # Load credentials
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_data = json.load(f)
        
        client_info = creds_data.get('web', creds_data.get('installed'))
        
        # Start local server
        try:
            server = socketserver.TCPServer(("", PORT), OAuthHandler)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            logger.info("Local server started on port %d", PORT)
        except Exception as e:
            logger.error("Failed to start local server: %s", e)
            logger.info("Falling back to manual mode")
            return self._setup_oauth_vps()
        
        # Generate authorization URL
        state = secrets.token_urlsafe(32)
        auth_params = {
            'response_type': 'code',
            'client_id': client_info['client_id'],
            'redirect_uri': f'http://localhost:{PORT}',
            'scope': ' '.join(SCOPES),
            'state': state,
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        auth_url = f"{client_info['auth_uri']}?{urlencode(auth_params)}"
        
        # Open browser
        print("\nOpening browser for authorization...")
        webbrowser.open(auth_url)
        
        print("Please login with Google Workspace administrator account")
        print("Waiting for authorization", end="", flush=True)
        
        # Wait for authorization
        timeout = 120
        start_time = time.time()
        
        while auth_code is None and (time.time() - start_time) < timeout:
            time.sleep(1)
            print(".", end="", flush=True)
        
        print()
        
        try:
            server.shutdown()
        except:
            pass
        
        if auth_code is None:
            logger.warning("Browser authorization timeout, falling back to manual mode")
            return self._setup_oauth_vps()
        
        logger.info("Authorization code received")
        return self._exchange_code_for_token(client_info, auth_code)
    
    def _setup_credentials(self) -> bool:
        """Setup OAuth2 credentials file"""
        if os.path.exists(CREDENTIALS_FILE):
            use_existing = input(f"\nFound existing {CREDENTIALS_FILE}. Use it? (y/n): ").lower()
            if use_existing == 'y':
                return True
            else:
                os.remove(CREDENTIALS_FILE)
        
        print("\nOAuth2 Credentials Setup")
        print("-" * 30)
        print("Prerequisites:")
        print("1. Admin SDK API enabled in Google Cloud Console")
        print("2. OAuth2 credentials created (Web application type)")
        print("3. Redirect URI added: http://localhost:8080")
        
        has_json = input("\nDo you have the credentials JSON file? (y/n): ").lower()
        
        if has_json == 'y':
            json_path = input("Enter path to JSON file: ").strip()
            if json_path.startswith('"') and json_path.endswith('"'):
                json_path = json_path[1:-1]
            
            try:
                with open(json_path, 'r') as f:
                    creds_data = json.load(f)
                with open(CREDENTIALS_FILE, 'w') as f:
                    json.dump(creds_data, f, indent=2)
                logger.info("Credentials saved successfully")
                return True
            except Exception as e:
                logger.error("Failed to load credentials file: %s", e)
                return False
        else:
            print("\nManual credential entry:")
            client_id = input("Client ID: ").strip()
            client_secret = input("Client Secret: ").strip()
            
            if not client_id or not client_secret:
                logger.error("Client ID and Secret are required")
                return False
            
            creds_data = {
                "web": {
                    "client_id": client_id,
                    "project_id": "google-workspace-bulk-email",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": ["http://localhost:8080"]
                }
            }
            
            with open(CREDENTIALS_FILE, 'w') as f:
                json.dump(creds_data, f, indent=2)
            logger.info("Credentials created successfully")
            return True
    
    def _exchange_code_for_token(self, client_info: Dict, auth_code: str) -> bool:
        """Exchange authorization code for access token"""
        import requests
        
        logger.info("Exchanging authorization code for access token")
        
        token_data = {
            'code': auth_code,
            'client_id': client_info['client_id'],
            'client_secret': client_info['client_secret'],
            'redirect_uri': 'http://localhost:8080',
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.post(client_info['token_uri'], data=token_data)
            response.raise_for_status()
            token_info = response.json()
            
            if 'error' in token_info:
                logger.error("Token error: %s", token_info.get('error_description', token_info['error']))
                return False
            
            # Save token
            expiry = datetime.utcnow() + timedelta(seconds=token_info.get('expires_in', 3600))
            
            token_json = {
                "token": token_info['access_token'],
                "refresh_token": token_info.get('refresh_token'),
                "token_uri": client_info['token_uri'],
                "client_id": client_info['client_id'],
                "client_secret": client_info['client_secret'],
                "scopes": SCOPES,
                "expiry": expiry.isoformat() + "Z"
            }
            
            with open(TOKEN_FILE, 'w') as f:
                json.dump(token_json, f, indent=2)
            
            logger.info("Access token saved successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to exchange code for token: %s", e)
            return False
    
    def authenticate(self) -> Optional[object]:
        """Authenticate with Google Workspace"""
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        
        creds = None
        
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            except Exception as e:
                logger.error("Failed to load token: %s", e)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())
                    logger.info("Token refreshed successfully")
                except Exception as e:
                    logger.error("Token refresh failed: %s", e)
                    if self.setup_oauth():
                        return self.authenticate()
                    return None
            else:
                logger.info("Authentication required")
                if self.setup_oauth():
                    return self.authenticate()
                return None
        
        return creds
    
    def generate_unique_email(self, first_name: str, last_name: str) -> str:
        """Generate unique email address"""
        base_email = f"{first_name.lower()}.{last_name.lower()}"
        email = f"{base_email}@{self.domain}"
        counter = 1
        
        while True:
            try:
                self.service.users().get(userKey=email).execute()
                # Email exists, try with number
                email = f"{base_email}{counter}@{self.domain}"
                counter += 1
            except:
                # Email doesn't exist, we can use it
                break
        
        return email
    
    def create_user(self, index: int, total: int) -> Optional[str]:
        """Create single user account"""
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        
        email = self.generate_unique_email(first_name, last_name)
        
        user_data = {
            "name": {
                "givenName": first_name,
                "familyName": last_name
            },
            "password": self.password,
            "primaryEmail": email,
            "changePasswordAtNextLogin": False
        }
        
        try:
            self.service.users().insert(body=user_data).execute()
            logger.info("[%d/%d] Created: %s", index, total, email)
            print(f"[{index}/{total}] ✓ {email}")
            return f"{email} | {self.password} | {first_name} {last_name}"
        except Exception as e:
            error_msg = str(e)
            if 'quotaExceeded' in error_msg:
                logger.warning("[%d/%d] Quota exceeded", index, total)
                print(f"[{index}/{total}] ⚠ Quota exceeded - please wait")
            else:
                logger.error("[%d/%d] Failed to create %s: %s", index, total, email, error_msg)
                print(f"[{index}/{total}] ✗ {email} - Failed")
            return None
    
    def save_results(self, results: List[str]) -> str:
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("GOOGLE WORKSPACE BULK EMAIL CREATION RESULTS\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Domain: {self.domain}\n")
            f.write("=" * 60 + "\n\n")
            f.write("Email | Password | Full Name\n")
            f.write("-" * 60 + "\n")
            for result in results:
                f.write(f"{result}\n")
        
        return filename
    
    def run(self):
        """Main execution method"""
        self.display_header()
        
        # Check dependencies
        if not self.check_dependencies():
            return
        
        # Import Google libraries after dependency check
        from googleapiclient.discovery import build
        
        # Create default files
        self.create_default_files()
        
        # Load configuration
        if not self.load_configuration():
            logger.error("Failed to load configuration")
            return
        
        # Display configuration
        print("Configuration:")
        print(f"  Domain: {self.domain}")
        print(f"  Password: {self.password}")
        print(f"  Name combinations: {len(self.first_names)} x {len(self.last_names)} = {len(self.first_names) * len(self.last_names)}")
        print()
        
        # Get number of accounts to create
        try:
            count = int(input("Number of accounts to create: "))
            if count <= 0:
                raise ValueError("Count must be positive")
        except ValueError as e:
            logger.error("Invalid input: %s", e)
            return
        
        # Authenticate
        print("\nAuthenticating...")
        creds = self.authenticate()
        if not creds:
            logger.error("Authentication failed")
            return
        
        # Build service
        self.service = build('admin', 'directory_v1', credentials=creds)
        logger.info("Connected to Google Workspace Admin SDK")
        
        # Create accounts
        print(f"\nCreating {count} accounts...")
        print("-" * 60)
        
        results = []
        success_count = 0
        failed_count = 0
        start_time = time.time()
        
        for i in range(1, count + 1):
            result = self.create_user(i, count)
            
            if result:
                results.append(result)
                success_count += 1
            else:
                failed_count += 1
            
            # Progress indicator
            if i % 10 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                eta = (count - i) / rate if rate > 0 else 0
                print(f"\nProgress: {i}/{count} ({(i/count)*100:.0f}%) - ETA: {int(eta)}s\n")
            
            # Rate limiting
            time.sleep(RATE_LIMIT_DELAY)
        
        # Save results
        if results:
            filename = self.save_results(results)
            print(f"\nResults saved to: {filename}")
        
        # Display summary
        elapsed_total = time.time() - start_time
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Successful: {success_count}/{count}")
        if failed_count > 0:
            print(f"  Failed: {failed_count}")
        print(f"  Duration: {int(elapsed_total)}s")
        if success_count > 0:
            print(f"  Rate: {success_count/elapsed_total:.2f} accounts/second")
        print("=" * 60)


def main():
    """Main entry point"""
    try:
        manager = GoogleWorkspaceManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        logger.info("Operation cancelled by user")
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        print(f"\nError: {e}")


if __name__ == '__main__':
    main()
