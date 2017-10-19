# Hardware Control
# Asynchronous Processing
We announce several decorators trying to implement transparency asynchronous abilities.

Inside `eva`, there will be several standalone processes, each process will handle one specific hardware-intensive job.
Take such code for example:
```python
from eva.hardware import cpu, network, io
from joblib import Parallel, delayed


class CrawlerSync(object):
    def __init__(self, url):
        self.url = url

    def download(self):
        # download contents of self.url
        pass

    def parse(self):
        # parse downloaded contents
        pass

    def export(self):
        # save into database
        pass

    def run(self):
        self.download()
        self.parse()
        self.export()


class CrawlerAsync(object):
    def __init__(self, url):
        self.url = url

    @network
    def download(self):
        # download contents of self.url
        pass

    @cpu
    def parse(self):
        # parse downloaded contents
        pass

    @io
    def export(self):
        # save into database
        pass

    def run(self):
        self.download()
        self.parse()
        self.export()


def sync_call():
    Parallel(n_jobs=10)(
        delayed(lambda x: CrawlerSync(x).run())(x)
        for x in url_list
    )


def async_call():
    Parallel(n_jobs=10)(
        delayed(lambda x: CrawlerAsync(x).run())(x)
        for x in url_list
    )
```

