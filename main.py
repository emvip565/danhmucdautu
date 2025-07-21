import os
import json
import time
import threading
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, Updater, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("7808035983:AAFhYC_3x0FMaNXQTCHPyjclAYWAoTlncSo")
CHAT_ID = os.getenv("1669162628")
PORTFOLIO_FILE = "portfolio.json"
CHECK_INTERVAL = 60  # giây

bot = Bot(token=TOKEN)

def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return {}
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f)

def get_price(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        res = requests.get(url)
        data = res.json()
        return data[coin_id]["usd"]
    except:
        return None

def get_total_value(portfolio):
    total = 0.0
    for coin, data in portfolio.items():
        price = get_price(coin)
        if price is None:
            continue
        total += price * data["amount"]
    return total

def add(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) != CHAT_ID:
        return
    if len(context.args) != 3:
        update.message.reply_text("Cú pháp: /add <coin_id> <số_lượng> <giá_mua>")
        return
    coin_id = context.args[0].lower()
    try:
        amount = float(context.args[1])
        buy_price = float(context.args[2])
    except:
        update.message.reply_text("Vui lòng nhập đúng định dạng số.")
        return
    portfolio = load_portfolio()
    portfolio[coin_id] = {"amount": amount, "buy_price": buy_price}
    save_portfolio(portfolio)
    update.message.reply_text(f"✅ Đã thêm {amount} {coin_id.upper()} với giá mua {buy_price} USD.")

def remove(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) != CHAT_ID:
        return
    if len(context.args) != 1:
        update.message.reply_text("Cú pháp: /remove <coin_id>")
        return
    coin_id = context.args[0].lower()
    portfolio = load_portfolio()
    if coin_id in portfolio:
        del portfolio[coin_id]
        save_portfolio(portfolio)
        update.message.reply_text(f"🗑️ Đã xoá {coin_id.upper()} khỏi danh mục.")
    else:
        update.message.reply_text("Không tìm thấy đồng coin này trong danh mục.")

def view(update: Update, context: CallbackContext):
    if str(update.effective_chat.id) != CHAT_ID:
        return
    portfolio = load_portfolio()
    if not portfolio:
        update.message.reply_text("Danh mục trống.")
        return
    msg = "📊 Danh mục đầu tư:
"
    total_buy = 0
    total_now = 0
    for coin, data in portfolio.items():
        price = get_price(coin)
        if price is None:
            continue
        value_now = price * data["amount"]
        value_buy = data["buy_price"] * data["amount"]
        total_now += value_now
        total_buy += value_buy
        msg += f"- {coin.upper()}: {data['amount']} @ {data['buy_price']} USD
"
        msg += f"  🔹 Giá hiện tại: {price} → Giá trị: {value_now:.2f} USD\n"
    profit = total_now - total_buy
    msg += f"\n💰 Tổng đầu tư: {total_buy:.2f} USD"
    msg += f"\n📈 Giá trị hiện tại: {total_now:.2f} USD"
    msg += f"\n📊 Lãi/Lỗ: {profit:.2f} USD"
    update.message.reply_text(msg)

def check_loop():
    last_value = None
    while True:
        try:
            portfolio = load_portfolio()
            current_value = get_total_value(portfolio)
            if last_value is not None and current_value != last_value:
                profit = current_value - sum(p["buy_price"] * p["amount"] for p in portfolio.values())
                message = (f"🔔 Biến động danh mục!
"
                           f"💼 Giá trị mới: {current_value:.2f} USD
"
                           f"📊 Lãi/Lỗ: {profit:.2f} USD")
                bot.send_message(chat_id=CHAT_ID, text=message)
            last_value = current_value
        except Exception as e:
            print(f"Lỗi khi kiểm tra danh mục: {e}")
        time.sleep(CHECK_INTERVAL)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("remove", remove))
    dp.add_handler(CommandHandler("view", view))

    threading.Thread(target=check_loop, daemon=True).start()
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
