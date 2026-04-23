import MetaTrader5 as mt
import pandas as pd
import datetime
import keyboard
import time

SYMBOL      = "EURUSD"
TIMEFRAME   = mt.TIMEFRAME_M15
MAGIC       = 1001
LOT         = 0.01
SL_PTS      = 200
TL_PTS      = 400
TF_SECS     = 15 * 60

def connect():
    if not mt.initialize():
        print("Failed to connect to your MT5 acc, ensure you downloaded the latest version of MetaTrader5")
        return False
    
    print(f"---------------------------------------")
    print(f"(✅) Connected to MetaTrader5.")

    selected = mt.symbol_select(SYMBOL, True)
    if not selected:
        print(f"Failed to select Symbol: {SYMBOL}.")
        return False
    else:
        print(f"(✅) Selected Symbol: {SYMBOL}")

    return True

def get_data(n=100):
    rates = mt.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, n)

    if rates is not None:
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        print(df.tail())
        print("\n")
        
        return df

# strategy goes here
def get_signal():
    return

def place_order():
    return

def sell_order():
    return

def run():
    if connect():
        print(f"(✅) Bot is running.")
        info = mt.account_info()
        print(f"Balance: ${info.balance:.2f}\n")
        time.sleep(3)

        while True:
            tick = mt.symbol_info_tick(SYMBOL)
            if tick is not None:
                tick_time = datetime.datetime.fromtimestamp(tick.time)
                print(f"Time: {tick_time}, Bid: {tick.bid}, Ask: {tick.ask}")

            df = get_data()

            time.sleep(1.5)
            if keyboard.is_pressed('q'):
                break

        print("Shutting down MetaTrader5")
        mt.shutdown()

if __name__ == "__main__":
    run()