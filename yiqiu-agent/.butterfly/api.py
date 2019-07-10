# coding=utf8
import os
import struct

from xlib import util
from xlib.httpgateway import Request
from xlib import retstat
from xlib import schema
from xlib import easyrun

from conf import logger_conf

__info__ = "meetbill"
__version__ = "1.0.1"
exe_path = os.path.split(os.path.realpath(__file__))[0]


def ping(req):
    """demo
    Args:
        req:
    Returns:
        httpstatus, [content], [headers]
        > httpstatus: 必须有
        > content: 非必须(当返回值为 2 个的时候，第 2 个返回值为 Content)
        > headers: 非必须(当返回值为 3 个的时候，第 3 个返回值为 headers)
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


def app(req, log_id, appinfo):
    """
    Args:
        log_id: log_id
        appinfo: (json)
    """
    isinstance(req, Request)
    if not _check_appinfo(appinfo):
        return retstat.ERR_BAD_PARAMS, {
            "log_id": log_id, "errinfo": "ERR_BAD_PARAMS"}, [(__info__, __version__)]
    req.log_params["exe_path"] = exe_path
    exe_commend = easyrun.run_capture(
        "python ./plugin/cli.py %s" %
        appinfo["action"])
    if not exe_commend.success:
        return retstat.ERR, {"log_id": log_id, "errinfo": exe_commend.output}, [
            (__info__, __version__)]
    return retstat.OK, {"log_id": log_id}, [(__info__, __version__)]
