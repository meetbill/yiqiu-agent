#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-07-07 10:58:55

# File Name: cli.py
# Description:

"""
import os
from server_manager import deploy as _deploy
from server_manager import schema
from server_manager import blog

root_path = os.path.split(os.path.realpath(__file__))[0]
os.chdir(root_path)
blog.init_log("../logs/hook")


def deploy(bundle="./data/example.zip"):
    """
    Args:
        bundle: The deploy archive file path
                it can be local file path or internet path.
    备注：
        执行 hook 脚本时会设置两个变量，service_tpl 可设置为任意名称：
        YIQIU_PROGRAM_HOME：service_tpl/program/
        YIQIU_UNIT_HOME：service_tpl/
    """
    if not schema.Schema(os.path.exists).is_valid(bundle):
        print "not found %s" % bundle
        sys.exit(-1)
    _deploy.Deploy().deploy(bundle)


if __name__ == '__main__':
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
