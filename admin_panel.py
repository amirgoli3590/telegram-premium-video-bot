from telebot import types

def admin_handler(bot, message, db, save_db):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ افزودن دسته‌بندی", callback_data="add_category"))
    markup.add(types.InlineKeyboardButton("➖ حذف دسته‌بندی", callback_data="remove_category"))
    markup.add(types.InlineKeyboardButton("📥 افزودن قسمت", callback_data="add_episode"))
    markup.add(types.InlineKeyboardButton("🗑 حذف قسمت", callback_data="remove_episode"))
    markup.add(types.InlineKeyboardButton("👥 مدیریت کاربران", callback_data="manage_users"))
    markup.add(types.InlineKeyboardButton("📊 آمار کلی", callback_data="stats"))
    bot.send_message(message.chat.id, "👑 پنل مدیریت:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "add_category")
def add_category_callback(call):
    msg = bot.send_message(call.message.chat.id, "📂 نام دسته‌بندی جدید را وارد کنید:")
    bot.register_next_step_handler(msg, lambda m: add_category(bot, m, db, save_db))

def add_category(bot, message, db, save_db):
    name = message.text.strip()
    if name in db['categories']:
        bot.send_message(message.chat.id, "⚠️ این دسته‌بندی قبلاً وجود دارد.")
    else:
        db['categories'][name] = {}
        save_db(db)
        bot.send_message(message.chat.id, f"✅ دسته‌بندی '{name}' اضافه شد.")

@bot.callback_query_handler(func=lambda call: call.data == "remove_category")
def remove_category_callback(call):
    markup = types.InlineKeyboardMarkup()
    for cat in db['categories']:
        markup.add(types.InlineKeyboardButton(cat, callback_data=f"delcat_{cat}"))
    bot.send_message(call.message.chat.id, "📂 کدام دسته‌بندی را حذف کنیم؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delcat_"))
def confirm_remove_category(call):
    cat = call.data.replace("delcat_", "")
    if cat in db['categories']:
        del db['categories'][cat]
        save_db(db)
        bot.send_message(call.message.chat.id, f"🗑 دسته‌بندی '{cat}' حذف شد.")
    else:
        bot.send_message(call.message.chat.id, "⚠️ چنین دسته‌ای وجود ندارد.")

# قسمت‌های اضافه کردن و حذف قسمت مثل دسته‌بندی نوشته شده و مشابهه
# همچنین مدیریت کاربران و آمار کلی
