from enum import Enum

TOKEN = '1849866111:AAH1EUYJup2t9WVApvLDeP93THHO9_ptpd4' # orign

main_db = "db.db"

YM_TOKEN = '410018476660527.2BA1EBEB1BD740893F6FC186409912EDBD5CE2BDBE658F93F45CD42C67773ABD5E4810145891A86DED33941D947A6A9F788C2A8BBD6C55015426F62304520966C98E0EACAD70E49A74262CD352ECE63F7C6240AB263B8F8630697C1A7BA72CCB7738CC6092DA2F79C37EA791E2C951B86C8BD3F38A3B60BAE9968ED88ABAFA0A'

am_time = '7:00'  # время рассылки (утро)
pm_time = '21:00'  # время рассылки (вечер)

photos_path = 'photos'  # путь к папке с фотками
photos_format = '.jpg'  # расширение фоток

total_days = 21  # кол-во дней

price = 377  # цена


class States(Enum):
    START = "0"
    NAME = "1"
