import time
import pyupbit
import datetime
import requests

access = "d"
secret = "d"
myToken = "d"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+ token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k # 시가 + 변동폭
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 시작 메세지 슬랙 전송
post_message(myToken,"#crypto", "autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SAND") # 9:00
        end_time = start_time + datetime.timedelta(days=1) # 9:00 + 1일

        # 9:00 
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-SAND", 0.7) # target_price(매수목표가)
            ma15 = get_ma15("KRW-SAND")
            current_price = get_current_price("KRW-SAND")
            if target_price < current_price and ma15 < current_price: # target보다 현재가가 높으면 매수
                krw = get_balance("KRW")
                if krw > 5000: # 잔고 5000원 이상일 때
                    buy_result = upbit.buy_market_order("KRW-SAND", krw*0.9995)
                    post_message(myToken,"#crypto", "SAND buy : " +str(buy_result))
        else:
            sand = get_balance("SAND") 
            if sand > 0.747: # 가지고 있는 sand가 5000원 이상이면 9시 10초전부터 전량 매도
                sell_result = upbit.sell_market_order("KRW-SAND", sand*0.9995) # 비트코인 수수료 고려해서 99.95%만 매도
                post_message(myToken,"#crypto", "SAND buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#crypto", e)
        time.sleep(1)