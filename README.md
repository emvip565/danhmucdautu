# 📈 Telegram Portfolio Tracker Bot

Bot Telegram theo dõi **toàn bộ danh mục đầu tư crypto** và gửi cảnh báo khi có **biến động**.

---

## ✅ Tính năng

- Cấu hình danh mục ngay trong Telegram:
  - `/add <coin_id> <số lượng> <giá mua>`
  - `/remove <coin_id>`
  - `/view`
- Theo dõi giá coin từ CoinGecko
- Tính tổng đầu tư, giá trị hiện tại, lãi/lỗ
- Gửi cảnh báo khi có biến động (không cần ngưỡng 5%)
- Lưu trữ vào file `portfolio.json`

---

## 🚀 Hướng dẫn triển khai

1. Tạo bot Telegram tại [BotFather](https://t.me/BotFather)
2. Lấy CHAT_ID bằng cách nhắn tin cho bot, rồi truy cập:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
3. Đẩy mã nguồn lên GitHub, sau đó deploy lên [Render.com](https://render.com/)
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
   - Loại service: Background Worker

---

## ⚙️ Cấu hình biến môi trường (`.env`)

| Biến | Ý nghĩa |
|------|--------|
| TELEGRAM_TOKEN | Token bot Telegram |
| CHAT_ID | ID Telegram người dùng được phép cấu hình danh mục |

---

💡 Mặc định chỉ bạn (CHAT_ID) được phép thao tác với bot để đảm bảo bảo mật.
