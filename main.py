import time
import yfinance as yf
from google import genai
import os

# API Key ماحول (Environment Variables) سے حاصل کی جائے گی
API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6JoLW-fhC51xQ8iZgZnRV6khNZpcoywddkmYU5VM6bg5Q")
client = genai.Client(api_key=API_KEY)

# ------------------- ڈمی والٹ (Virtual Wallet) -------------------
balance_usdt = 1000.0  # $1,000 ڈمی بیلنس
crypto_holdings = 0.0
symbol = "BTC-USD"

print(f"💰 ڈمی ٹریڈنگ بوٹ کلاؤڈ پر شروع ہو گیا!")
print(f"شروعاتی بیلنس: ${balance_usdt:.2f} USDT\n")

def run_bot_cycle():
    global balance_usdt, crypto_holdings
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")
        current_price = data['Close'].iloc[-1]
        
        prompt = f"""
        آپ ایک خودکار ٹریڈنگ بوٹ ہیں۔
        کوائن: {symbol}
        موجودہ قیمت: ${current_price:.2f}
        پچھلے 5 دن کا ڈیٹا:
        {data[['Open', 'High', 'Low', 'Close']].to_string()}
        
        مندرجہ ذیل فارمیٹ میں صرف ایک لفظ کی کمانڈ اور مختصر وجہ لکھیں:
        Action: BUY یا SELL یا HOLD
        Reason: وجہ
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        analysis = response.text
        print(f"\n📊 [{time.strftime('%Y-%m-%d %H:%M:%S')}] {symbol} قیمت: ${current_price:.2f}")
        print(f"🤖 AI کا فیصلہ: {analysis.strip()}")
        
        if "Action: BUY" in analysis and balance_usdt >= 50:
            buy_amount = 50
            crypto_holdings = buy_amount / current_price
            balance_usdt -= buy_amount
            print(f"✅ [خریداری]: ${buy_amount} کا BTC خریدا گیا۔ نیا بیلنس: ${balance_usdt:.2f}")
            
        elif "Action: SELL" in analysis and crypto_holdings > 0:
            sell_value = crypto_holdings * current_price
            balance_usdt += sell_value
            print(f"🔴 [فروخت]: BTC ${sell_value:.2f} میں بیچے گئے۔ نیا بیلنس: ${balance_usdt:.2f}")
            crypto_holdings = 0.0
            
        else:
            print("⏳ [ہولڈ]: فی الحال کوئی ٹریڈ نہیں لی گئی۔")

    except Exception as e:
        print(f"❌ غلطی: {e}")

# 24/7 مسلسل چلنے والا لوپ (ہر 1 گھنٹے بعد چکر لگائے گا)
while True:
    run_bot_cycle()
    time.sleep(3600)  # 3600 سیکنڈ = 1 گھنٹہ
