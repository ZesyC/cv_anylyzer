# Hướng dẫn thiết lập Gemini API

## Lấy API Key miễn phí

1. Truy cập: **https://aistudio.google.com/app/apikey**
2. Đăng nhập với Google Account
3. Click "**Create API Key**"
4. Copy API key (dạng: `AIzaSy...`)

## Cài đặt API Key

### Bước 1: Tạo file `.env`

```bash
cd backend
cp .env.example .env
```

### Bước 2: Điền API Key

Mở file `backend/.env` và thay thế `API key` bằng API key thật của bạn:

```env
# Thay "API key" bằng API key thật từ Google AI Studio
GEMINI_API_KEY=AIzaSyABCD1234_your_real_api_key_here

# Model (khuyên dùng gemini-1.5-flash cho tốc độ)
GEMINI_MODEL=gemini-1.5-flash
```

### Bước 3: Restart Backend

```bash
# Ctrl+C để stop backend hiện tại
# Sau đó chạy lại:
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

## Kiểm tra hoạt động

### Test 1: Xem logs

Khi upload CV, check terminal logs:

-  Nếu thấy: `"Using Gemini API (gemini-1.5-flash) for CV analysis in vi"` → **Thành công!**
-  Nếu thấy: `"Gemini API not configured, using mock feedback"` → API key chưa đúng

### Test 2: Upload CV

1. Upload một file CV
2. Kết quả sẽ khác với mock data cũ
3. Feedback sẽ cụ thể dựa trên nội dung CV thật

## Xử lý lỗi

### Lỗi: "API key not valid"

- Kiểm tra lại API key có đúng không
- Đảm bảo không copy nhầm dấu cách
- API key phải bắt đầu với `AIzaSy`

### Lỗi: "Resource exhausted" (Rate limit)

- Free tier: 15 requests/minute
- Đợi 1 phút rồi thử lại
- Hoặc giảm tần suất test

### Fallback to Mock

Nếu Gemini API fails (network, rate limit, etc.), hệ thống tự động quay về mock data - không bị crash!

## Free Tier Limits

**Gemini 1.5 Flash** (Recommended):

-  15 requests/minute
-  1 million tokens/minute
-  1,500 requests/day
- ⚡ Rất nhanh

**Gemini 1.5 Pro** (Nếu cần chất lượng cao hơn):

-  2 requests/minute
-  32,000 tokens/minute
- Chỉnh trong `.env`: `GEMINI_MODEL=gemini-1.5-pro`

## Gỡ bỏ API (quay về Mock)

Nếu muốn tắt Gemini và dùng mock data:

1. Xóa/comment API key trong `.env`:

   ```env
   # GEMINI_API_KEY=API key
   ```

2. Hoặc set về placeholder:

   ```env
   GEMINI_API_KEY=API key
   ```

3. Restart backend

---

Có vấn đề? Check logs ở terminal backend để debug!
