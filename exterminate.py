# ----------------------------------------------------------------
# 导入库
# ----------------------------------------------------------------
import time
import json
import math
import sys


def addExterminate(json_file_name):

    # 剿灭日志文件
    exter_log_file_name = 'log/exter_log.json'

    # 基准时间不动 time.time()要加上时区偏移
    start_time = (4.0*24)*60*60     # 1970-01-05 00:00:00
    current_time = time.time()+8*60*60
    current_week = int((current_time - start_time) / 60 / 60 / 24 / 7)
    print('剿灭添加模块： 今天是第', current_week, '周')

    # 读入要添加剿灭的配置文件
    json_file = open(json_file_name, 'r', encoding='utf-8')
    json_conf = json_file.read()
    json_file.close()

    accounts_list = json.loads(json_conf)

    # 查看日志
    exter_log_file = open(exter_log_file_name, 'r', encoding='utf-8')
    exter_log = exter_log_file.read()
    exter_log_file.close()

    exter_log = json.loads(exter_log)

    # 如果当前周在日志中，则添加过了剿灭
    if str(current_week) in exter_log:
        print('剿灭添加模块： 本周写入过了，结束写入', current_week)
        return

    # 剿灭没添加过的状态，开始添加剿灭
    extermax_list = {1: 255, 2: 325, 3: 345}
    for acc in accounts_list:
        # 生成一个临时字典
        dictemp = dict()
        extermax = accounts_list[acc]['extermax']
        exterminate = accounts_list[acc]['exterminate']
        # 计算剿灭次数
        exter_number = math.ceil(extermax / extermax_list[exterminate])
        dictemp['jm-'+str(exterminate)] = exter_number
        dictemp.update(accounts_list[acc]['todo'])
        accounts_list[acc]['todo'] = dictemp
    # 添加完剿灭 开始写入文件
    json_conf = json.dumps(accounts_list,
                           ensure_ascii=False,
                           indent=4)
    json_file = open(json_file_name, 'w', encoding='utf-8')
    json_file.write(json_conf)
    json_file.close()

    # 添加剿灭完成 写入剿灭添加日志
    # 写入log里周数以及具体时间
    exter_log[str(current_week)] = time.strftime("%Y-%m-%d %H:%M:%S %w",
                                                 time.localtime())
    exter_log = json.dumps(exter_log,
                           ensure_ascii=False,
                           indent=4)
    exter_log_file = open(exter_log_file_name, 'w', encoding='utf-8')
    exter_log_file.write(exter_log)
    exter_log_file.close()


def main(argv):
    if len(argv) == 0:
        print('剿灭添加模块： 请输入要写入文件')
        return
    addExterminate(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
