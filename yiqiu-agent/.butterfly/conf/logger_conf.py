#coding:utf8

from xlib import logger
import config

# 通用 logging 初始化
logger.init_log(config.PATH_COMMON_LOG)

critlog = logger.LoggerBase(config.PATH_CRIT_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

errlog = logger.LoggerBase(config.PATH_ERR_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

warninglog = logger.LoggerBase(config.PATH_WARNING_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

infolog = logger.LoggerBase(config.PATH_INFO_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)

acclog = logger.LoggerBase(config.PATH_ACC_LOG, False, config.LOG_SIZE_LIMIT, config.LOG_BATCH_WRITE)
