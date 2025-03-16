import os

import pandas as pd
from config import settings


def export_exel(contact_list):
    os.mkdir(os.path.join(settings.MEDIA_ROOT, "exported"))
    path = os.path.join(settings.MEDIA_ROOT, "exported/contact_list.xlsx")
    df = pd.DataFrame(contact_list)
    df.to_excel(path, index=False)
    return 'exported/contact_list.xlsx'
