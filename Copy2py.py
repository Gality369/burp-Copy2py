# coding=utf-8

from burp import IBurpExtender
from burp import IParameter
from burp import IContextMenuFactory
from burp import IBurpExtenderCallbacks

from javax.swing import JMenu
from javax.swing import JMenuItem

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Copy2py")
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, invocation):
        if invocation.getToolFlag() == IBurpExtenderCallbacks.TOOL_REPEATER or IBurpExtenderCallbacks.TOOL_PROXY:
            menu = []
            menu.append(JMenuItem("Copy to py", None, actionPerformed=lambda x, y=invocation: self.copy2py(x, y)))

        return menu

    def copy2py(self,event, invocation):
        for HttpRequestResponse in invocation.getSelectedMessages():

            request = HttpRequestResponse.getRequest()
            httpService = HttpRequestResponse.getHttpService()
            analyze_request = self._helpers.analyzeRequest(httpService, request)

            # 设置参数
            params = {}
            headers = {}
            data = {}
            avoidList = ['Connection','Cache-Control','Host','Accept-Encoding','Accept-Language','Accept','Content-Type']
            paramList = analyze_request.getParameters()

            url = str(analyze_request.getUrl()).split("?")[0]
            for header in analyze_request.getHeaders():
                try:
                    if header.split(':')[0] in avoidList:
                        continue
                    headers[header.split(':')[0]] = header.split(':')[1].strip()
                except IndexError:
                    continue
            for param in paramList:
                if param.getType() == IParameter.PARAM_BODY:
                    data[param.getName()] = param.getValue()
                elif param.getType() == IParameter.PARAM_URL:
                    params[param.getName()] = param.getValue()


            # 格式化打印
            print("import requests\n")
            print("url = '" + url + "'")
            if params:
                print("params = {")
                for (key, value) in params.items():
                    print("    '" + key + "': '" + value + "',")
                print("}")
            if data:
                print("data = {")
                for (key, value) in data.items():
                    if key != '':
                        print("    '" + key + "': '" + value + "',")
                print("}")
            if headers:
                print("headers = {")
                try:
                    for (key, value) in headers.items():
                        print("    '" + key + "': '" + value + "',")
                    print("}\n")
                except:
                    pass

            if analyze_request.getMethod() == 'GET':
                print("r = requests.get(url, params=params, headers=headers)")
            elif analyze_request.getMethod() == 'POST':
                print("r = requests.post(url, data=data,headers=headers)")
            print("print(r.status_code)")
            print("print(r.content)")