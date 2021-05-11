import time
from monitor import *
import logging
import argparse
import os
import sys

################
###CONSTANTS###
VERSION_NUM = '0.88.1'

IP = '127.0.0.1'
PORT = 5088
###############

### Arguments###
argParser = argparse.ArgumentParser()
argParser.add_argument("model", help="The location of the model used as the oracle.", default = "model/mascot-safety-system.csp")
argParser.add_argument("map", help="The location of the event map", default = "event_map.json")
argParser.add_argument("type", help="The type of check to be performed", choices=['offline', 'online'])
argParser.add_argument("-n", "--name", help="The name of the check and therefore name of the log file")
argParser.add_argument("-t", "--trace_file", help="The location of the trace file. Only used if type='offline'")
argParser.add_argument("-s", "--speed", help="Run 10 timed run and produce the times and mean.).", type=bool, default = False)

args = argParser.parse_args()

MODEL = args.model
MAP = args.map
TYPE = args.type
SPEED_CHECK = args.speed
TRACE_FILE = args.trace_file
if args.name:
    CHECK_NAME = args.name
else:
    CHECK_NAME = "scenario x"
#TODO check and warn for incompatible params

################
#set to the name of the scenario
logFileName = args.name
log_level = logging.INFO

if not os.path.exists("log"):
    os.mkdir("log")

varanus_logger = logging.getLogger("varanus")
varanus_logger.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fileHandler = logging.FileHandler("log/varanus-"+logFileName+"-"+time.strftime("%Y_%m_%d-%H:%M:%S")+ ".log")

fileHandler.setFormatter(formatter)

varanus_logger.addHandler(fileHandler)

print("+++++++++++++++++++++++")
print("+++++++ VARANUS +++++++")
print("++++ version " + str(VERSION_NUM) + " +++")
print("++++ Matt Luckcuck ++++")
print("+++++++++++++++++++++++")
print("")



varanus_logger.debug("Varanus Running v" + str(VERSION_NUM))

varanus_logger.info("+++ Testing " + logFileName + " +++")

if SPEED_CHECK == False:
# NORMAL USAGE

    #mon.run_offline_rosmon("../rosmon-test/rosmon-mascot-pass.json")
    #mon._run_offline_traces("trace.json")

    if TYPE == "offline":
        t0 = time.time()
        mon = Monitor(MODEL, MAP)
        mon._run_offline_traces_single(TRACE_FILE)
    elif TYPE == "online":
        t0 = time.time()
        mon = Monitor(MODEL, MAP)
        mon.run_online_traces_accumulate(IP, PORT, timeRun=False)

    #mon.run_online('127.0.0.1', 5044)
    #mon.run_online_websocket('127.0.0.1', 8080)
    mon.close()
    t1 = time.time()

    total = t1-t0

    varanus_logger.info("+++ Time: "+ str(total) +"s +++")

    varanus_logger.debug("Varanus Finished")
elif SPEED_CHECK == True:
# SPEED CHECK USAGE
# Like mascot-speed-test.py but inside Varanus
    varanus_logger.info("+++ SPEED CHECK +++")
    sys.path.append("../mascot-test/")
    from mascot_speed_test import write_csv

    SOURCE_LIST = ["scenario1-trace", "scenario2-trace", "scenario2a-trace", "scenario2b-trace",
    "scenario3-trace", "scenario4-trace", "scenario4a-trace", "scenario4b-trace", "scenario5-trace",
    "scenario6-trace", "scenario7-trace", "scenario0-10-trace", "scenario0-100-trace", "scenario0-1000-trace",
    "scenario0-10000-trace", "scenario0-100000-trace"]

    times = []

    if TYPE == "offline":
        OUTPUT_DIR = "../mascot-test/offline-times/"

        #for scenario_name in SOURCE_LIST[0:2]:

        varanus_logger.info("+++ SCENARIO:" + CHECK_NAME + " +++")

        for i in range(10):
            t0 = time.time()

            mon = Monitor(MODEL, MAP)
            mon._run_offline_traces_single(TRACE_FILE)
            mon.close()

            t1 = time.time()
            total = t1-t0
            times.append(total)



        write_csv(CHECK_NAME, times, OUTPUT_DIR)


    elif TYPE == "online":
        OUTPUT_DIR = "../mascot-test/online-times/"

        for scenario_name in SOURCE_LIST[0:2]:
            print ("SCENARIO:" + scenario_name)

            for i in range(10):
                mon.run_online_traces_accumulate(IP, PORT, timeRun=True)
