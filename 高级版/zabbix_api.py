#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib.request
import urllib.parse

class ZabbixAPI(object):
    #单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ZabbixAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self, url, user, password):
        self.__header = {"Content-Type": "application/json"}
        self.__data = {"jsonrpc": "2.0", "method": "", "params": "", "id": 1}
        self.url = url
        self.__data['auth'] = self.__login(user, password)

    def __login(self, user, password):
        method = 'user.login'
        params = {"user": user, "password": password}
        auth = self.deal_request(method, params)

        return auth

    def deal_request(self, method, params):
        '''
        发起http请求
        :param method: zabbix请求方法，例：'host.get'
        :param params: zabbix请求参数，例：{'output': 'extend'}
        :return: 请求结果
        '''
        self.__data["method"] = method
        self.__data["params"] = params
        data = bytes(json.dumps(self.__data), 'utf8')
        request = urllib.request.Request(url=self.url, data=data, headers=self.__header)
        response = urllib.request.urlopen(request)
        try:
            res = json.loads(response.read().decode('utf-8'))
            return res["result"]
        except Exception:
            raise Exception

    def __getattr__(self, name):
        return ZabbixObj(name, self)

class ZabbixObj(object):
    def __init__(self, method_fomer, ZabbixAPI):
        self.method_fomer = method_fomer
        self.ZabbixAPI = ZabbixAPI

    def __getattr__(self, name):
        def func(params):
            method = self.method_fomer+"."+name
            params = params
            return  self.ZabbixAPI.deal_request(method=method,params=params)
        return func

if __name__ == '__main__':
    zbx = ZabbixAPI('http://192.168.50.13/zabbix/api_jsonrpc.php', 'Admin', 'dVxUPN04UQNYTj4InNmV')
    print(zbx.host.get({'output': "extend"}))
