import time
from monitor import *
import logging
import argparse
import os

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

print("+++++++++++++++++++++")
print("++++++ VARANUS ++++++")
print("++++ version " + str(VERSION_NUM) + " ++++")
print("+++ Matt Luckcuck +++")
print("+++++++++++++++++++++")
print("")



varanus_logger.debug("Varanus Running v" + str(VERSION_NUM))

varanus_logger.info("+++ Testing " + logFileName + " +++")

if SPEED_CHECK == False:
# NORMAL USAGE
    t0 = time.time()
    mon = Monitor(MODEL, MAP)
    #mon.run_offline_rosmon("../rosmon-test/rosmon-mascot-pass.json")
    #mon._run_offline_traces("trace.json")

    if TYPE == "offline":
        mon._run_offline_traces_single(TRACE_FILE)
    elif TYPE == "online":
        mon.run_online_traces_accumulate(IP, PORT, timeRun=True)

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
    SOURCE_LIST = ["scenario1-trace", "scenario2-trace", "scenario2a-trace", "scenario2b-trace",
    "scenario3-trace", "scenario4-trace", "scenario4a-trace", "scenario4b-trace", "scenario5-trace",
    "scenario6-trace", "scenario7-trace", "scenario0-10-trace", "scenario0-100-trace", "scenario0-1000-trace",
    "scenario0-10000-trace", "scenario0-100000-trace"]

    fdr.library_init()

    if TYPE == "offline":
        OUTPUT_DIR = "../mascot-test/offline-times/"

        mon._run_offline_traces_single("../mascot-test/scenario-traces/scenario1-trace.json")
    elif TYPE == "online":
        OUTPUT_DIR = "../mascot-test/online-times/"


        mon.run_online_traces_accumulate(IP, PORT, timeRun=True)





        for scenario_name in SOURCE_LIST[0:2]:
            pass

        fdr.library_exit()
