# -*- coding: utf8 -*-
import json
import requests
from download_center.new_spider.downloader import config


class ProxyDeal(object):

    def get_proxy(self, data):
        # 获取代理 ip
        r = requests.post(config.AGENCYIP_URL.format(config.DOWNLOADER_CENTER_IP[config.ENVIR]),
                          data=data, timeout=config.REQUEST_TIMEOUT)
        return json.loads(r.text)["proxy"]

    def delete_proxy(self, proxies):
        # 删除失效代理ip
        AgencyIp = str(proxies["http"].split("://")[-1])
        data = {
            "AgencyIp": AgencyIp
        }
        r = requests.post(config.DELETE_IP_URL.format(config.DOWNLOADER_CENTER_IP[config.ENVIR]),
                          data=data, timeout=config.REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.text
        else:
            return "代理池删除ip【{}】失败".format(AgencyIp)
