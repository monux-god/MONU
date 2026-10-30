#!/usr/bin/env python3
"""
MONU PAPA BOT - Master Executor
Fixed: Removed unlimited_cmd handler
"""
print("--- [DEBUG] Script started ---")

import sys
import logging
import warnings
import traceback

try:
    print("--- [DEBUG] Importing modules... ---")
    import config
    import utils
    import database
    from states import State
    from handlers import (
        start, number, telegram, aadhar, 
        credits, referral, payment, admin, callbacks, call2
    )
    from telegram import Update
    from telegram.ext import (
        Application, CommandHandler, CallbackQueryHandler, 
        MessageHandler, filters, ContextTypes
    )
    print("--- [DEBUG] All modules imported successfully ---")
except Exception as e:
    print(f"--- [ERROR] Import failed: {e} ---")
    traceback.print_exc()
    sys.exit(1)

# ==============================================================================
# SYSTEM LOGGING
# ==============================================================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=UserWarning)

# ==============================================================================
# GLOBAL FSM ROUTER
# ==============================================================================
async def handle_fsm_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not update.message:
        return
    
    if await start.is_user_banned(user.id):
        return

    state = context.user_data.get('state')
    text = update.message.text.strip() if update.message.text else ""

    if text.startswith('/'):
        if text == "/cancel":
            context.user_data['state'] = None
            await update.message.reply_text(f"❌ Operation aborted")
        return

    # ===== ADMIN ROUTES =====
    if user.id == config.OWNER_ID:
        if state == State.ADMIN_BROADCAST:
            await admin.perform_broadcast(update, context)
            return
        
        if state == State.ADMIN_ADD_UNLIMITED_ID:
            await admin.admin_add_unlimited_id_recv(update, context)
            return

    # ===== PAYMENT ROUTE =====
    if state == State.WAIT_PAYMENT_PROOF:
        await payment.handle_payment_proof(update, context)
        return

    # ===== SEARCH ROUTES =====
    if not text:
        return

    if state == State.WAIT_NUMBER:
        await number.process_number_search(update, context, text)
        context.user_data['state'] = None
    elif state == State.WAIT_TG:
        await telegram.process_tg_search(update, context, text, text)
        context.user_data['state'] = None
    elif state == State.WAIT_AADHAR:
        await aadhar.process_aadhar_search(update, context, text)
        context.user_data['state'] = None

# ==============================================================================
# ERROR HANDLER
# ==============================================================================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        error = context.error
        print(f"--- [ERROR] {error} ---")
        traceback.print_exc()
        
        if update and update.effective_user:
            try:
                if update.message:
                    await update.message.reply_text(
                        "⚠️ *Something went wrong*\n\nPlease try again or contact support.",
                        parse_mode="Markdown"
                    )
                elif update.callback_query:
                    await update.callback_query.answer("⚠️ Error occurred", show_alert=True)
            except:
                pass
    except:
        pass

# ==============================================================================
# MAIN EXECUTION ENGINE
# ==============================================================================
def main():
    print("--- [DEBUG] Entering main() function ---")
    try:
        utils.init_project()
        print("--- [DEBUG] Project initialized ---")
        
        app = Application.builder().token(config.BOT_TOKEN).build()
        print("--- [DEBUG] Application built ---")

        # Command handlers
        app.add_handler(CommandHandler("start", start.start))
        app.add_handler(CommandHandler("help", start.start))
        app.add_handler(CommandHandler(["admin", "panel", "dashboard"], admin.admin_dashboard))
        app.add_handler(CommandHandler("broadcast", admin.broadcast_command))
        app.add_handler(CommandHandler("adddays", admin.add_days_command))
        app.add_handler(CommandHandler("search", admin.search_user))
        app.add_handler(CommandHandler("proxy", credits.website_proxy))
        app.add_handler(CommandHandler("bomber", call2.bomber_start))
        app.add_handler(CommandHandler("addcredits", admin.add_credits_cmd))
        
        # Callback handler
        app.add_handler(CallbackQueryHandler(callbacks.callback_handler))
        
        # Message handler
        app.add_handler(MessageHandler(
            (filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | 
             filters.ANIMATION | filters.Sticker.ALL | filters.FORWARDED) & ~filters.COMMAND, 
            handle_fsm_logic
        ))
        
        # Error handler
        app.add_error_handler(error_handler)
        print("--- [DEBUG] All handlers registered ---")

        print(f"🚀 {config.BOT_NAME} SUPREME ENGINE LIVE 👑")
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"--- [CRITICAL ERROR] Bot failed to start: {e} ---")
        traceback.print_exc()

if __name__ == "__main__":
    main()