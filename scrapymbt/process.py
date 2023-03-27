from scrapymbt.settings import *


# 文本处理：返回关键字和关键字个数
class Value:
    def __init__(self, _str, _list):
        self._str = _str
        self._list = _list

    # 返回单个关键字
    def process_value(self):
        for j in self._list:
            if j in self._str:
                return j

    # 本方法仅返回单个关键字
    def return_value(self):
        # 返回品牌和项目
        if self._list == BRAND or self._list == PROJECT or self._list == BIG_BRAND or self._list == SMALL_BRAND:
            return Value.process_value(self)

        # 用于返回政策类资讯标题关键字，暂时无用
        if self._list == PROVINCE_POLICY_KW:
            is_deleted = None
            for i in PROVINCE_POLICY_DELETED_KW:
                if i in self._str:
                    is_deleted = i
            if is_deleted is not None:
                return None
            else:
                return Value.process_value(self)

        # 返回省份
        if self._list == PROVINCE:
            province = Value.process_value(self)
            # 若匹配出省份名，则直接返回值，否则需要根据地级市判断省份
            if province is not None:
                return province
            else:
                for i in HEBEI:
                    if i in self._str:
                        return "河北"
                for i in SHANXI:
                    if i in self._str:
                        return "山西"
                for i in LIAONING:
                    if i in self._str:
                        return "辽宁"
                for i in JILIN:
                    if i in self._str:
                        return "吉林"
                for i in HEILONGJIANG:
                    if i in self._str:
                        return "黑龙江"
                for i in JIANGSU:
                    if i in self._str:
                        return "江苏"
                for i in ZHEJIANG:
                    if i in self._str:
                        return "浙江"
                for i in ANHUI:
                    if i in self._str:
                        return "安徽"
                for i in FUJIAN:
                    if i in self._str:
                        return "福建"
                for i in JIANGXI:
                    if i in self._str:
                        return "江西"
                for i in SHANDONG:
                    if i in self._str:
                        return "山东"
                for i in HENAN:
                    if i in self._str:
                        return "河南"
                for i in HUBEI:
                    if i in self._str:
                        return "湖北"
                for i in HUNAN:
                    if i in self._str:
                        return "湖南"
                for i in GUANGDONG:
                    if i in self._str:
                        return "广东"
                for i in HAINAN:
                    if i in self._str:
                        return "海南"
                for i in SICHUAN:
                    if i in self._str:
                        return "四川"
                for i in GUIZHOU:
                    if i in self._str:
                        return "贵州"
                for i in YUNNAN:
                    if i in self._str:
                        return "云南"
                for i in SHAANXI:
                    if i in self._str:
                        return "陕西"
                for i in GANSU:
                    if i in self._str:
                        return "甘肃"
                for i in QINGHAI:
                    if i in self._str:
                        return "青海"
                for i in NEIMENGGU:
                    if i in self._str:
                        return "内蒙古"
                for i in GUANGXI:
                    if i in self._str:
                        return "广西"
                for i in XIZANG:
                    if i in self._str:
                        return "西藏"
                for i in NINGXIA:
                    if i in self._str:
                        return "宁夏"
                for i in XINJIANG:
                    if i in self._str:
                        return "新疆"

        # 返回产品类型
        if self._list == PRODUCT:
            if '空气能' in self._str:
                return "空气源热泵"
            else:
                return Value.process_value(self)

        # 返回内容分类，暂时没用
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

    # 本方法返回多个关键字，用于返回政策类资讯标题和内容的多个关键字
    def return_multi_kw(self):
        result = None
        for i in self._list:
            if i in self._str:
                if result is None:
                    result = i
                else:
                    result = result + "," + i
        return result

    # 用于计算政策类资讯标题/内容包含关键词的数量
    def keyword_count(self):
        count = 0
        for j in self._list:
            if j in self._str:
                count = count + 1
        return count

# 找到第nth个str在source_str中的index
class FindStr:
    def __init__(self, source_str, str, nth):
        self.source_str = source_str
        self.str = str
        self.nth = nth

    def return_nth_place(self):
        count = 0
        index = 0
        for i in self.source_str:
            index = index + 1
            if i == self.str:
                count = count + 1
            if count == self.nth:
                return index

