# coding=utf8
import os
import struct
import schema

from xlib import util
from xlib.httpgateway import Request
from xlib import retstat
from xlib.middleware import funcattr
from xlib import easyrun

__info__ = "meetbill"
__version__ = "1.0.1"

exe_path = os.path.split(os.path.realpath(__file__))[0]

@funcattr.api
def ping(req):
    """demo
    Args:
        req:
    Returns:
        当此函数作为简单接口函数返回时:
            json_status, [content], [headers]
            > json_status: (int,str)必须有，实际返回给用户时，json_status 也会放到 json 串中
            > content: (dict)非必须(当返回值为 2 个的时候，第 2 个返回值为 Content)
            > headers: 非必须(当返回值为 3 个的时候，第 3 个返回值为 headers)
        当此函数作为 HTTP 方法返回时:
            httpstatus, [content], [headers]
            > httpstatus: (int)必须有
            > content: (str/dict)非必须(当返回值为 2 个的时候，第 2 个返回值为 Content)
                       当 content 为 dict 时，会自动转为 json ，并且设置 header("Content-Type","application/json")
                       当 content 为其他时，会自动设置为 ("Content-Type","text/html")
            > headers: 非必须(当返回值为 3 个的时候，第 3 个返回值为 headers)

        如下例子为简单接口函数
    """
    isinstance(req, Request)
    req.log_params["x"] = 1
    clen = struct.unpack("i", os.urandom(4))[0] % 64 + 64
    randstr = util.Base64_16.bin_to_b64(os.urandom(clen))
    return retstat.OK, {"randstr": randstr}, [(__info__, __version__)]


def _check_appinfo(appinfo):
    """Check whether the parameters are legitimate
    Args:
        appinfo:(dict)
    Returns:
        bool
    """
    rules = {
        "action": schema.And(lambda n: n in ["deploy"], error="action ind deploy")
    }
    return schema.Schema(rules).is_valid(appinfo)


@funcattr.api
def app(req, log_id, appinfo):
    """
    Args:
        log_id: log_id
        appinfo: (json)
    """
    isinstance(req, Request)
    if not _check_appinfo(appinfo):
        return retstat.ERR_BAD_PARAMS, {"log_id": log_id, "errinfo": "ERR_BAD_PARAMS"}, [(__info__, __version__)]
    req.log_params["exe_path"] = exe_path
    exe_commend = easyrun.run_capture("python ./plugin/cli.py %s" % appinfo["action"])
    if not exe_commend.success:
        return retstat.ERR, {"log_id": log_id, "errinfo": exe_commend.output}, [(__info__, __version__)]
    return retstat.OK, {"log_id": log_id}, [(__info__, __version__)]
