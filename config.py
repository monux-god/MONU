#!/usr/bin/env python3
"""
MONU PAPA - Master Configuration
Placeholder Version - Ready to Share
"""

import os

# ========== BOT CORE SETTINGS ==========
# 🔴 CHANGE THIS - Apna bot token daalo
BOT_TOKEN = "8828874398:AAHJzESSUiUYYoFfJbABjsdSh396Yqml4n4"

BOT_USERNAME = "MONU_BABU_XBOT" 
BOT_NAME = "MONU PAPA"

# ========== OWNER & SUPPORT ==========
OWNER_ID = 5866168507
OWNER_USERNAME = "@itz_stylish_m0nu"
SUPPORT_GROUP = "@MONU_X"
CHANNEL_TG = "@MONUNAAP"
OWNER_TG = "@itz_stylish_m0nu"
GROUP_TG = "@MONU_X"
RAW_OWNER_NUMBER = "918853414988"
WHATSAPP_CHANNEL_LINK = "https://whatsapp.com/channel/0029Vb7VTiKGZNCv3pOYaL1x"

# ========== API GATEWAY ==========
API_KEY = "AayanOp"
NUM_API_URL = "https://aayan-info7.vercel.app/api/lookup"
TG_API_URL = "https://raixinfo3.vercel.app/api/tg"
AADHAR_API_URL = "https://raiixinfo.vercel.app/get_data"


# ========== STORAGE PATHS ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
LOG_DIR = os.path.join(BASE_DIR, "logs")

USERS_DB = os.path.join(DB_DIR, "users.json")
CREDITS_DB = os.path.join(DB_DIR, "credits.json")
REFERRAL_DB = os.path.join(DB_DIR, "referrals.json")
COOLDOWN_DB = os.path.join(DB_DIR, "cooldown.json")
PAYMENTS_DB = os.path.join(DB_DIR, "payments.json")
SEARCH_HISTORY = os.path.join(LOG_DIR, "searches.json")

# ========== SYSTEM LIMITS ==========
REF_REQUIRED = 2  # 2 Refer = 1 Search

NUM_CD = 120
TG_CD = 10
AADHAR_CD = 60

# ========== PAYMENT & PLANS ==========
# 🔴 CHANGE THIS - Apna UPI ID daalo
UPI_ID = "monukk5265-2@okhdfcbank"
QR_IMAGE = "https://ibb.co/HTDSfT5k"

PLANS = {
    "weekly": {"price": 49, "days": 7, "label": "📅 WEEKLY → ₹49 (7 Days)"},
    "monthly": {"price": 129, "days": 30, "label": "📅 MONTHLY → ₹129 (30 Days)"},
    "yearly": {"price": 399, "days": 365, "label": "👑 YEARLY → ₹399 (365 Days)"}
}

# ========== UI DECORATION ==========
DIVIDER = "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
HEADER_LINE = DIVIDER
FOOTER_LINE = DIVIDER

# ========== MEMBERSHIP ==========
# 🔴 CHANGE THIS - Apne channels daalo
REQUIRED_CHATS = ["@MONU_X"]
CHANNEL_LINKS = [
   
    "https://t.me/@MONUNAAP"
]