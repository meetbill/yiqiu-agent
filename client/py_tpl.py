#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-06-17 22:14:42

# File Name: py_tpl.py
# Description:

"""
import urllib2
import json

"""
request = urllib2.Request("http://127.0.0.1:8585/ping")
#request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
response = urllib2.urlopen(request)
# 返回码
print "ret_code:",response.getcode()
print "url:",response.geturl()
# 返回内容
print "content:",response.read()
# 请求id，此 id 会打印到 butterfly 日志中
print "x-reqid:",response.info().getheader('x-reqid')
# 请求耗时
print "x-cost:",response.info().getheader('x-cost')
"""
# put


def put():
    pass
# deploy


def deploy():
    return_info = {}
    log_id = 123456
    return_info["log_id"] = log_id
    url = "http://127.0.0.1:4001/api/app?log_id=%s" % log_id
    # 处理所有参数
    json_data = {
        "appinfo": {
            "action": "deploy"
        },
    }
    data = json.dumps(json_data)

    headers = {"User-Agent": "Mozilla....", "Content-Type": "application/json"}
    request = urllib2.Request(url, data=data, headers=headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        return_info["stat"] = "ERR"
        return_info["x-reqid"] = e.headers.getheader('x-reqid')
        return_info["x-cost"] = e.headers.getheader('x-cost')
        if e.code == 400:
            return_info["err_info"] = "HTTP Error 400: Bad Request"
            return return_info
        else:
            return_info["err_info"] = e.reason
            return return_info

    content = json.loads(response.read())
    return_info["x-reqid"] = response.headers.getheader('x-reqid')
    return_info["x-cost"] = response.headers.getheader('x-cost')
    return_info["stat"] = content["stat"]
    if content["stat"] == "OK":
        pass
    else:
        pass
    return return_info


if __name__ == "__main__":
    import sys
    import inspect
    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                        str(["%s=%s" % (a, b) for a, b in zip(
                            args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[
                        1:-1].replace(",", "")
        sys.exit(-1)
    else:
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
            print r
        except Exception as e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(
                func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip()
                                 for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
