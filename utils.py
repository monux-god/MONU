#!/usr/bin/env python3
"""
MONU PAPA BOT - Master Utility Engine
"""

import os
import json
import re
from datetime import datetime
import config

def sc(text: str) -> str:
    if not text:
        return ""
    mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ',
        'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ',
        'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
        's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅',
        '6': '₆', '7': '₇', '8': '₈', '9': '₉'
    }
    return "".join(mapping.get(c.lower(), c) for c in str(text))

def escape(text: str) -> str:
    if not text:
        return ""
    reserved = r'_*[]()~`>#+-=|{}.!'
    for char in reserved:
        text = str(text).replace(char, f"\\{char}")
    return text

def init_project():
    if not os.path.exists(config.DB_DIR):
        os.makedirs(config.DB_DIR)
    if not os.path.exists(config.LOG_DIR):
        os.makedirs(config.LOG_DIR)
    
    schemas = {
        config.USERS_DB: {},
        config.CREDITS_DB: {},
        config.REFERRAL_DB: {},
        config.COOLDOWN_DB: {},
        config.PAYMENTS_DB: [],
        config.SEARCH_HISTORY: []
    }

    for path, structure in schemas.items():
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(structure, f, indent=4)
            print(f"✅ Initialized: {os.path.basename(path)}")

def clean_text(text):
    if text is None or str(text).lower() in ["none", "null", "n/a", ""]:
        return sc("not available")
    return str(text).strip()

def clean_address(address):
    if not address or str(address).lower() in ["none", "null", ""]:
        return sc("not available")
    address = str(address).replace('!', ', ').replace('_', ' ')
    address = re.sub(r',+', ', ', address)
    return address.strip(', ')[:120]

def get_timestamp():
    now = datetime.now()
    return now.timestamp(), now.strftime("%Y-%m-%d %H:%M:%S")

def get_now():
    return get_timestamp()[1]

def log_event(event_type: str, details: str, user_id: int = 0):
    try:
        with open(config.SEARCH_HISTORY, 'r+', encoding='utf-8') as f:
            logs = json.load(f)
            logs.append({
                "time": get_now(),
                "user_id": user_id,
                "type": event_type,
                "details": details
            })
            if len(logs) > 5000:
                logs = logs[-5000:]
            f.seek(0)
            json.dump(logs, f, indent=4)
            f.truncate()
    except Exception:
        pass

def log_search(user_id, search_type, target, status):
    log_event(f"{search_type}_{status}", f"Target: {target}", user_id)