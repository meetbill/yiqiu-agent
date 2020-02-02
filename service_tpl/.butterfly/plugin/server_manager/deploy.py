#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import urllib2
import subprocess
import zipfile
import logging

from poyo import parse_string


class Deploy(object):
    """
     Attributes:
        _bundle:*.zip
        _cur_dir: cli.py 所在目录，即 .../service_tpl/.butterfly/plugin
        _bundle_dir：bundle 为网络包时的下载路径
        _program_dir：bundle 的解压路径，即 .../service_tpl/program
        _workdir: 服务目录，即服务标准化中服务的工作目录，即 .../service_tpl/

    备注：
        service_tpl 可自定义为其他名称
    """
    def __init__(self):

        self._bundle = None
        self._cur_dir = os.getcwd()
        self._bundle_dir = os.path.join(self._cur_dir, "data")
        if not os.path.isdir(self._bundle_dir):
            os.makedirs(self._bundle_dir)
        self._program_dir = os.path.join(self._cur_dir, "../../program")
        self._workdir = os.path.join(self._cur_dir, "../../")

    def unzip_bundle(self):
        """unzip_bundle"""
        zf = zipfile.ZipFile(self._bundle, "r")
        zf.extractall(self._program_dir)

    def deploy(self, bundle):
        """ Deploy a service
        Args:
            bundle: Service Package
        """
        logging.info("DownloadBundle...")
        self.download_bundle(bundle)
        zf = zipfile.ZipFile(self._bundle, "r")
        #appspec = yaml.load(zf.read("appspec.yml"))
        appspec = parse_string(zf.read("appspec.yml"))
        zf.close()
        self.unzip_bundle()

        workdir = appspec.get("workdir")
        if workdir is not None:
            self._workdir = workdir
        if not os.path.isdir(self._program_dir):
            os.makedirs(self._program_dir)

        logging.info("RUN ApplicationStop...")
        self._exec_hooks(appspec.get("hooks").get("ApplicationStop"))

        logging.info("RUN BeforeInstall...")
        self._exec_hooks(appspec.get("hooks").get("BeforeInstall"))

        logging.info("RUN Install...")
        self.install(appspec.get("files"))

        logging.info("RUN AfterInstall...")
        self._exec_hooks(appspec.get("hooks").get("AfterInstall"))

        logging.info("RUN ApplicationStart...")
        self._exec_hooks(appspec.get("hooks").get("ApplicationStart"))

        logging.info("RUN ValidateService...")
        self._exec_hooks(appspec.get("hooks").get("ValidateService"))

        logging.info("Deploy OK.")

    def _exec_hooks(self, hooks):
        if hooks is None:
            return
        try:
            for hook in hooks:
                self._run_cmd(hook["location"])
        except Exception as err:
            raise Exception("run cmd error: " + repr(err))

    def _run_cmd(self, cmd):
        cmd_new = "export YIQIU_PROGRAM_HOME=%s;export YIQIU_UNIT_HOME=%s;bash %s" % (
            self._program_dir, self._workdir, cmd)
        p = subprocess.Popen(
            cmd_new,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self._program_dir)
        while p.poll() is None:
            line = p.stdout.readline()
            logging.info(line.strip())
        rc = p.returncode
        if rc != 0:
            logging.warn("rc: " + str(rc))
            logging.warn("stderr: " + p.stderr.read())
            raise Exception("run cmd error.")
        return rc

    def download_bundle(self, bundle):
        """download_bundle
        Args:
            bundle:*.zip
        """
        if bundle.startswith("http://"):
            f = urllib2.urlopen(bundle)
            self._bundle = os.path.join(
                self._bundle_dir, os.path.basename(bundle))
            with open(self._bundle, "wb") as zf:
                zf.write(f.read())
        else:
            self._bundle = bundle

    def install(self, files):
        if files is None:
            return
        zf = zipfile.ZipFile(self._bundle, "r")
        for entry in files:
            source = entry["source"]
            destination = entry["destination"]
            if source == "/":
                zf.extractall(self._workdir)
            elif source in zf.namelist():
                zf.extract(source, self._workdir)
            else:
                source = source.endswith("/") and source or source + "/"
                for f in zf.namelist():
                    if f.startswith(source):
                        zf.extract(f, self._workdir)
        zf.close()
