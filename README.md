# burp-copy2py

该burp插件可以使得将burp的请求直接保存成可执行的py脚本的形式,节省了输入参数等的编程时间,方便在自定义sql盲注脚本时快速生成一个可用的框架.

## 使用

- BurpLog2py

  python3 BurpLog2py.py burplog OutputFileName

- Copy2py

  先在burp中加载该插件,输出方式选择save to file并指定一个空py文件

  在proxy或repeater页面选择Copy to py