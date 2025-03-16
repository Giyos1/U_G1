# import requests
#
# url = "http://127.0.0.1:8000/book/create/"
#
# data = {
#     "title": "Alo",
#     "author": 2
# }
#
# response = requests.post(url, json=data)
# print(response.status_code)
import os.path

import pandas as pd
# from config import settings


def export_exel(contact_list):
    path = os.path.join( "exported/contact_list.xlsx")
    df = pd.DataFrame(contact_list)
    df.to_excel(path, index=False)
    return path


if __name__ == "__main__":
    export_exel([
        {
            "name": "Ali",
            "email": "ali@mail.com",
            "phone": "9989989898",
            "address": "Tashkent"
        },
        {
            "name": "Ali",
            "email": "ali@mail.com",
            "phone": "9989989898",
            "address": "Tashkent"
        },
        {
            "name": "Ali",
            "email": "ali@mail.com",
            "phone": "9989989898",
            "address": "Tashkent"
        }
    ])
