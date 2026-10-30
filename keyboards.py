#!/usr/bin/env python3
"""
MONU PAPA BOT - Elite UI Component Manager
New System: Plans + Referral Searches
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import sc
import config

def back_button(callback_data="menu_main"):
    return [InlineKeyboardButton(f"🔙 Back", callback_data=callback_data)]

def back_keyboard(callback_data="menu_main"):
    return InlineKeyboardMarkup([back_button(callback_data)])

def home_button():
    return [InlineKeyboardButton(f"🏠 Home", callback_data="menu_main")]

def main_keyboard():
    """Main dashboard with new buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🔍 Number Info", callback_data="nav_number"),
            InlineKeyboardButton(f"👤 Telegram Info", callback_data="nav_tg")
        ],
        [
            InlineKeyboardButton(f"🪪 Aadhar Family", callback_data="nav_aadhar"),
            InlineKeyboardButton(f"📞 CALL BOMBER", callback_data="bomber_menu")
        ],
        [
            InlineKeyboardButton(f"💎 My Plan", callback_data="menu_plan"),
            InlineKeyboardButton(f"🎁 Referral", callback_data="menu_referral")
        ],
        [
            InlineKeyboardButton(f"💰 Buy Plan", callback_data="menu_plans"),
            InlineKeyboardButton(f"⚙️ Help", callback_data="menu_help")
        ]
    ])

def plan_keyboard():
    """Show user's plan status"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🛒 Buy Plan", callback_data="menu_plans")],
        back_button()
    ])

def plans_keyboard():
    """Plans - Weekly, Monthly, Yearly"""
    buttons = []
    for plan_id, info in config.PLANS.items():
        buttons.append([InlineKeyboardButton(info['label'], callback_data=f"buy_{plan_id}")])
    buttons.append(back_button("menu_main"))
    return InlineKeyboardMarkup(buttons)

def payment_confirm_keyboard(plan_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"✅ I Have Paid", callback_data=f"paid_{plan_id}")],
        [InlineKeyboardButton(f"🔙 Change Plan", callback_data="menu_plans")]
    ])

def force_join_keyboard():
    buttons = []
    for i, link in enumerate(config.CHANNEL_LINKS, 1):
        buttons.append([InlineKeyboardButton(f"📢 Join Channel {i}", url=link)])
    buttons.append([InlineKeyboardButton(f"✅ Verify Membership", callback_data="verify_join")])
    return InlineKeyboardMarkup(buttons)

def referral_keyboard(ref_code):
    share_url = f"https://t.me/share/url?url=https://t.me/{config.BOT_USERNAME}?start={ref_code}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔗 Share Link", url=share_url)],
        back_button()
    ])

def result_keyboard():
    return InlineKeyboardMarkup([
        home_button()
    ])

def no_search_keyboard():
    """When user has no searches left"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🎁 Refer Now", callback_data="menu_referral"),
            InlineKeyboardButton(f"💰 Buy Plan", callback_data="menu_plans")
        ],
        home_button()
    ])

# ==============================================================================
# ADMIN KEYBOARDS
# ==============================================================================
def admin_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"📊 Live Stats", callback_data="adm_stats"),
            InlineKeyboardButton(f"👥 User Database", callback_data="adm_users")
        ],
        [
            InlineKeyboardButton(f"📢 Broadcast", callback_data="adm_broadcast"),
            InlineKeyboardButton(f"💳 Payments", callback_data="adm_payments")
        ],
        [
            InlineKeyboardButton(f"🚀 Add Unlimited Days", callback_data="adm_add_days"),
            InlineKeyboardButton(f"🔍 Search User", callback_data="adm_search_user")
        ],
        [
            InlineKeyboardButton(f"🛠 Maintenance", callback_data="adm_maint"),
            InlineKeyboardButton(f"❌ Close Dashboard", callback_data="close_admin")
        ]
    ])

def admin_add_days_keyboard():
    """Custom days + preset buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("♾️ LIFETIME", callback_data="adddays_lifetime"),
            InlineKeyboardButton("📅 365 DAYS", callback_data="adddays_365")
        ],
        [
            InlineKeyboardButton("📅 30 DAYS", callback_data="adddays_30"),
            InlineKeyboardButton("📅 7 DAYS", callback_data="adddays_7")
        ],
        [
            InlineKeyboardButton("📅 1 DAY", callback_data="adddays_1"),
            InlineKeyboardButton("✏️ CUSTOM", callback_data="adddays_custom")
        ],
        [
            InlineKeyboardButton("🔙 BACK", callback_data="adm_main")
        ]
    ])

def admin_payment_action_keyboard(user_id, plan_id, days, price):
    payload = f"{user_id}|{plan_id}|{days}|{price}"
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"✅ Approve", callback_data=f"pay_apprv_{payload}"),
            InlineKeyboardButton(f"❌ Reject", callback_data=f"pay_rejct_{payload}")
        ],
        [
            InlineKeyboardButton(f"🚫 Block User", callback_data=f"adm_ban_{user_id}")
        ]
    ])

def admin_payments_keyboard(payments):
    buttons = []
    pending = [p for p in payments if p.get("status") == "Pending"]
    
    if not pending:
        buttons.append([InlineKeyboardButton("✅ No Pending Payments", callback_data="adm_main")])
    else:
        for p in pending[:5]:
            uid = p.get("uid", "Unknown")
            plan = p.get("plan", "Unknown")
            buttons.append([
                InlineKeyboardButton(
                    f"👤 {uid} - {plan.upper()}",
                    callback_data=f"adm_pay_view_{uid}"
                )
            ])
    
    buttons.append(back_button("adm_main"))
    return InlineKeyboardMarkup(buttons)