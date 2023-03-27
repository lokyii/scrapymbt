# 处理每月初收集的行业和政策信息
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

now = datetime.date.today()
# 本月1号
this_month_first_day = datetime.datetime(now.year, now.month, 1)
# 上个月1号
last_month_last_day = this_month_first_day - timedelta(days=1)

month_of_last_month = last_month_last_day.month
year_of_last_month = last_month_last_day.year

# 输入文件
input_fp = f"D:\\MyData\\7.信息汇总\\{year_of_last_month}\\{month_of_last_month}月\\info_hub.csv"
# 输出文件
output_fp = f"D:\\MyData\\7.信息汇总\\{year_of_last_month}\\{month_of_last_month}月\\info_hub_output.csv"

# 读取输入文件
df = pd.read_csv(input_fp, encoding="utf-8")
# 删除无用列
df = df.drop(["_id", "crawl_date"], axis=1)
# 调整列顺序
df = df[["website_type", "website", "brand", "big_brand", "small_brand", "product", "project", "province", "keywords",
         "created_date", "url", "title", "content"]]
# 排序
df.sort_values(by=["website_type", "website", "created_date"], ascending=[False, True, False], inplace=True)
# 删除标题重复的行
df = df.drop_duplicates(subset=["title"])


# 资讯类处理
#  判断brand=生能是否为政策信息，判断规则为：keywords列有“生能”，则brand和small_brand值不变，否则brand和small_brand列需修改为null
# 判断是否不包含关键字
def if_not_exists(a, k):
    if a is np.nan:
        return True
    if isinstance(a, str):
        if k not in a:
            return True
    return False


# 判断是否包含关键字
def if_exists(a, k):
    if a is np.nan:
        return False
    if isinstance(a, str):
        if k in a:
            return True
    return False


title_list = ["国家标准", "行业标准", "团体标准", "国标"]
content_list = ["PUE", "耗能", "节能", "能耗"]


def if_exists_in_list(a, l):
    if a is not np.nan:
        for k in l:
            if k in a.upper():
                return True
    return False


df["brand"] = df.apply(
    lambda x: None if (if_not_exists(x["keywords"], "生能") and x["website_type"] == "行业门户" and x["brand"] == "生能") else
    x["brand"], axis=1)
df["small_brand"] = df.apply(
    lambda x: x["brand"] if (x["small_brand"] == "生能" and x["website_type"] == "行业门户") else x["small_brand"], axis=1)

#   brand和small_brand=“新科”或者“英特”，keywords列有“新科”或“英特”则值不变，否则改为null
df["brand"] = df.apply(
    lambda x: None if (if_not_exists(x["keywords"], "新科") and x["website_type"] == "行业门户" and x["brand"] == "新科") else
    x["brand"], axis=1)
df["small_brand"] = df.apply(
    lambda x: x["brand"] if (x["small_brand"] == "新科" and x["website_type"] == "行业门户") else x["small_brand"], axis=1)
df["brand"] = df.apply(
    lambda x: None if (if_not_exists(x["keywords"], "英特") and x["website_type"] == "行业门户" and x["brand"] == "英特") else
    x["brand"], axis=1)
df["brand"] = df.apply(
    lambda x: "英特尔" if (if_exists(x["keywords"], "英特尔") and x["website_type"] == "行业门户" and x["brand"] == "英特") else
    x["brand"], axis=1)
df["small_brand"] = df.apply(
    lambda x: x["brand"] if (x["small_brand"] == "英特" and x["website_type"] == "行业门户") else x["small_brand"], axis=1)

#   数据中心类信息
#   新建列“是否数据中心类信息？”
df["is DC info?"] = df.apply(lambda x: "DC" if (x["website"][:4] == "IDC圈" or x["website"] == "数据中心节能技术委员会") else None,
                             axis=1)
#    新建列“数据中心类包含kw？”，若标题列不包含“国家标准”、“行业标准”、“团体标准”或“国标”，并且内容列不包含”PUE“、”耗能“或”节能“，则值为删除
df["DC info contains kw?"] = df.apply(lambda x: "保留" if x["is DC info?"] == "DC"
                                                        and (if_exists_in_list(x["title"],
                                                                               title_list) or if_exists_in_list(
    x["content"], content_list)) else None,
                                      axis=1)

#  keywords列有招标、经销商、零售商、旗舰店的行删掉
boolean = df.keywords.str.contains("招标|经销商|零售商|旗舰店|旗舰展示中心|专营店|体验店|专卖店|展厅|开店|开业|比武", na=False)
df = df[~boolean]

#  政策类处理
policy_list = ["绿色", "低碳", "减碳", "降碳", "碳中和", "碳达峰", "减排", "双碳", "零碳", "工业提升", "空调", "制冷", "热泵", "PUE", "数据中心", "采暖",
               "供暖", "新风机", "热负荷管理", "地热", "煤改", "清洁能源", "能效", "能耗", "能源", "节能", "旧改", "国家标准",
               "标准", "国标", "循环发展", "冷链", "冷藏"]
filter_list = ["批复", "公报", "招标", "中标", "审查意见", "采购", "新能源汽车"]
df["policy info contains kw?"] = df.apply(lambda x: "保留" if x["website_type"] == "政策法规"
                                                            and (if_exists_in_list(x["title"],
                                                                                   policy_list) and not if_exists_in_list(
    x["title"], filter_list)) else None,
                                          axis=1)

print(df)
df.to_csv(output_fp)
