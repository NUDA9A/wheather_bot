from threading import Thread
from bot import run_bot
from rest_api import run_rest_api

if __name__ == '__main__':
    Thread(target=run_rest_api).start()
    run_bot()
