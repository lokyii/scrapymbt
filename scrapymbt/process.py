from scrapymbt.settings import *


# 返回关键字
class Value:
    def __init__(self, _str, _list):
        self._str = _str
        self._list = _list

    def process_value(self):
        for j in self._list:
            if j in self._str:
                return j

    def return_value(self):
        if self._list == BRAND or self._list == PROJECT:
            return Value.process_value(self)

        if self._list == PROVINCE:
            for i in SHANDONG_CITY:
                if i in self._str:
                    return "山东"
                else:
                    return Value.process_value(self)

        if self._list == PRODUCT:
            if '空气能' in self._str:
                return "空气源热泵"
            else:
                return Value.process_value(self)

        if self._list == KEYWORD_TAB:
            for i in HEATING:
                if i in self._str:
                    return "采暖"
            for i in REPLACE_COAL:
                if i in self._str:
                    return "煤改"
            for i in SUBSIDY:
                if i in self._str:
                    return "补贴"
            for i in ECO_DATA:
                if i in self._str:
                    return "经济数据"
            for i in POLICY:
                if i in self._str:
                    return "政策"

            return Value.process_value(self)





