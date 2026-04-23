import MetaTrader5 as mt
import pandas as pd
import datetime
import keyboard
import asyncio

SYMBOL = "EURUSD"
TF     = mt.TIMEFRAME_M15
MAGIC  = 1001
LOT    = 0.01
SL_PTS = 200
TL_PTS = 400
TF_SECS = 15 * 60


async def main():
    if not mt.initialize():
        print("Failed to connect")
        return

    info = mt.account_info()
    print(f"[DEBUG]: Connected! Balance: {info.balance}\n")
    print("[SERVER]: Press 'q' to exit program.\n\n")
    
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def on_quit():
        print("\n[SYSTEM]: 'q' pressed. Initiating shutdown...\n")
        loop.call_soon_threadsafe(stop_event.set)

    keyboard.add_hotkey('q', on_quit)

    while not stop_event.is_set():
        tick = mt.symbol_info_tick("EURUSD")
        if tick is not None:
            tick_time = datetime.datetime.fromtimestamp(tick.time)
            print(f"[CURRENT]: Symbol: EURUSD, Bid: {tick.bid}, Ask: {tick.ask}, {tick_time}")

        rates = mt.copy_rates_from_pos(
            "EURUSD",
            mt.TIMEFRAME_M15,
            0,
            100
        )

        if rates is not None:
            df = pd.DataFrame(rates)
            df["time"] = pd.to_datetime(df["time"], unit="s")
            print(df.tail())
            print("\n")

        try:

            await asyncio.wait_for(stop_event.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            pass

    keyboard.remove_hotkey('q')
    mt.shutdown()
    print("Program ended successfully.")

if __name__ == "__main__":
    asyncio.run(main())