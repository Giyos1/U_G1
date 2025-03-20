import os
import pandas as pd
import time
from config import settings
import threading


def export_exel(contact_list, username):
    time_ = time.time()
    thread = threading.Thread(target=work, args=(contact_list, username, time_))
    thread.start()
    return f'exported/{username}/contact_list_{time_}.xlsx'


def work(contact_list, username, time):
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, f"exported/{username}")):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, f"exported/{username}"))

    path = os.path.join(settings.MEDIA_ROOT, f"exported/{username}/contact_list_{time}.xlsx")
    df = pd.DataFrame(contact_list)
    df.to_excel(path, index=False, engine='openpyxl')
