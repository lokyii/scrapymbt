from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings


# 自定义command
class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        # 获取爬虫列表
        spider_list = self.crawler_process.spiders.list()
        # 遍历各爬虫
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
            print("此时启动的爬虫：" + name)
        self.crawler_process.start()