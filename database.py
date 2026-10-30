#!/usr/bin/env python3
"""
MONU PAPA BOT - Database Manager
New System: Searches from referrals + Unlimited days from plans
"""

import json
import os
import shutil
import hashlib
from datetime import datetime
import config

def _load_json(path):
    try:
        if not os.path.exists(path):
            return {} if "payments" not in path and "searches" not in path else []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {} if "payments" not in path and "searches" not in path else []

def _save_json(path, data):
    try:
        if os.path.exists(path):
            shutil.copy2(path, path + ".backup")
        temp_path = path + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(temp_path, path)
        return True
    except Exception as e:
        print(f"--- [ERROR] Failed to save {path}: {e} ---")
        return False

# ==============================================================================
# USER MANAGEMENT
# ==============================================================================
def update_user_stats(user_id, username, first_name):
    users = _load_json(config.USERS_DB)
    uid = str(user_id)
    now_ts = datetime.now().timestamp()
    if uid not in users:
        users[uid] = {
            "first_seen": now_ts,
            "last_seen": now_ts,
            "username": username or "None",
            "first_name": first_name or "User",
            "total_searches": 0,
            "is_banned": False
        }
    else:
        users[uid]["last_seen"] = now_ts
        users[uid]["username"] = username or users[uid].get("username", "None")
        users[uid]["first_name"] = first_name or users[uid].get("first_name", "User")
    _save_json(config.USERS_DB, users)
    return users[uid]

# ==============================================================================
# USER STATUS (UNLIMITED + SEARCHES)
# ==============================================================================
def get_user_status(user_id):
    """Returns user's unlimited status and available searches"""
    credits = _load_json(config.CREDITS_DB)
    uid = str(user_id)
    now_ts = datetime.now().timestamp()
    
    if uid not in credits:
        credits[uid] = {
            "unlimited_until": 0,
            "searches": 0,          # Referral se mili searches
            "refer_count": 0,       # Kitne refer kiye
            "last_ref_credited": 0  # Last kitne refer pe search mili
        }
        _save_json(config.CREDITS_DB, credits)
    
    user_data = credits[uid]
    
    # Check unlimited
    is_unlimited = False
    expiry_date = "N/A"
    if user_data.get("unlimited_until", 0) > now_ts:
        is_unlimited = True
        expiry_date = datetime.fromtimestamp(user_data["unlimited_until"]).strftime("%Y-%m-%d %H:%M")
    
    return {
        "is_unlimited": is_unlimited,
        "expiry": expiry_date,
        "searches": user_data.get("searches", 0),
        "refer_count": user_data.get("refer_count", 0)
    }

def use_search(user_id, search_type="num"):
    """
    Use 1 search from referral searches.
    Returns True if search is available.
    """
    credits = _load_json(config.CREDITS_DB)
    uid = str(user_id)
    now_ts = datetime.now().timestamp()
    
    if uid not in credits:
        return False
    
    user_data = credits[uid]
    
    # Unlimited - no search needed
    if user_data.get("unlimited_until", 0) > now_ts:
        _increment_search_count(user_id)
        return True
    
    # Check searches available
    searches = user_data.get("searches", 0)
    if searches > 0:
        user_data["searches"] = searches - 1
        _save_json(config.CREDITS_DB, credits)
        _increment_search_count(user_id)
        return True
    
    return False

def _increment_search_count(user_id):
    users = _load_json(config.USERS_DB)
    uid = str(user_id)
    if uid in users:
        users[uid]["total_searches"] = users[uid].get("total_searches", 0) + 1
        _save_json(config.USERS_DB, users)

# ==============================================================================
# REFERRAL SYSTEM (2 Refer = 1 Search)
# ==============================================================================
def get_ref_data(user_id, username):
    refs = _load_json(config.REFERRAL_DB)
    uid = str(user_id)
    if uid not in refs:
        code = f"ref_{user_id}_{hashlib.md5(uid.encode()).hexdigest()[:6]}"
        refs[uid] = {
            "code": code,
            "count": 0,
            "referred_users": [],
            "username": username or "None"
        }
        _save_json(config.REFERRAL_DB, refs)
    return refs[uid]

def process_referral(new_user_id, ref_code):
    """Process referral. 2 Refer = 1 Search"""
    refs = _load_json(config.REFERRAL_DB)
    new_uid = str(new_user_id)
    referrer_id = None
    
    for rid, data in refs.items():
        if data.get("code") == ref_code:
            referrer_id = rid
            break
    
    if not referrer_id:
        return False, "Invalid referral code"
    if referrer_id == new_uid:
        return False, "You cannot refer yourself"
    
    for rid, data in refs.items():
        if new_user_id in data.get("referred_users", []):
            return False, "Already referred by someone"
    
    # Add referral
    refs[referrer_id]["count"] = refs[referrer_id].get("count", 0) + 1
    refs[referrer_id]["referred_users"].append(new_user_id)
    _save_json(config.REFERRAL_DB, refs)
    
    # 2 Refer = 1 Search
    credits = _load_json(config.CREDITS_DB)
    uid = referrer_id
    if uid not in credits:
        credits[uid] = {"unlimited_until": 0, "searches": 0, "refer_count": 0, "last_ref_credited": 0}
    
    credits[uid]["refer_count"] = credits[uid].get("refer_count", 0) + 1
    
    # Check if 2 refer completed
    total_refs = credits[uid]["refer_count"]
    last_credited = credits[uid].get("last_ref_credited", 0)
    
    if total_refs - last_credited >= config.REF_REQUIRED:
        credits[uid]["searches"] = credits[uid].get("searches", 0) + 1
        credits[uid]["last_ref_credited"] = total_refs
        _save_json(config.CREDITS_DB, credits)
        return True, f"+1 Search Unlocked! ({total_refs} referrals)"
    
    _save_json(config.CREDITS_DB, credits)
    remaining = config.REF_REQUIRED - (total_refs - last_credited)
    return True, f"Referral added! {remaining} more for +1 Search"

# ==============================================================================
# ADMIN: ADD UNLIMITED DAYS
# ==============================================================================
def add_unlimited(user_id, days):
    """Admin adds unlimited days to user"""
    credits = _load_json(config.CREDITS_DB)
    uid = str(user_id)
    
    if uid not in credits:
        credits[uid] = {"unlimited_until": 0, "searches": 0, "refer_count": 0, "last_ref_credited": 0}
    
    now = datetime.now().timestamp()
    current_expiry = credits[uid].get("unlimited_until", 0)
    base_time = max(now, current_expiry)
    credits[uid]["unlimited_until"] = base_time + (days * 86400)
    _save_json(config.CREDITS_DB, credits)
    return True

def remove_unlimited(user_id):
    """Admin removes unlimited access"""
    credits = _load_json(config.CREDITS_DB)
    uid = str(user_id)
    if uid in credits:
        credits[uid]["unlimited_until"] = 0
        _save_json(config.CREDITS_DB, credits)
    return True

# ==============================================================================
# COOLDOWN
# ==============================================================================
def check_cooldown(user_id, search_type):
    status = get_user_status(user_id)
    if status["is_unlimited"]:
        return True, 0
    
    cooldowns = _load_json(config.COOLDOWN_DB)
    uid = str(user_id)
    now = datetime.now().timestamp()
    cd_map = {"num": config.NUM_CD, "tg": config.TG_CD, "aadhar": config.AADHAR_CD}
    cd_time = cd_map.get(search_type, 60)
    key = f"{uid}_{search_type}"
    
    if key in cooldowns:
        elapsed = now - cooldowns[key]
        if elapsed < cd_time:
            return False, int(cd_time - elapsed)
    
    cooldowns[key] = now
    _save_json(config.COOLDOWN_DB, cooldowns)
    return True, 0

# ==============================================================================
# BACKWARD COMPATIBILITY
# ==============================================================================
def get_user_quota(user_id):
    """For backward compatibility"""
    status = get_user_status(user_id)
    return {
        "is_unlimited": status["is_unlimited"],
        "expiry": status["expiry"],
        "searches": status["searches"],
        "total": status["searches"]
    }

def add_credits(user_id, amount):
    """For backward compatibility - adds searches"""
    credits = _load_json(config.CREDITS_DB)
    uid = str(user_id)
    if uid not in credits:
        credits[uid] = {"unlimited_until": 0, "searches": 0, "refer_count": 0, "last_ref_credited": 0}
    credits[uid]["searches"] = credits[uid].get("searches", 0) + amount
    _save_json(config.CREDITS_DB, credits)
    return True