import time
from monitor import *
import logging
import os

################
###CONSTANTS###
VERSION_NUM = 0.6

###############

logFileName = "test"

if not os.path.exists("log"):
    os.mkdir("log")

varanus_logger = logging.getLogger("varanus")
varanus_logger.setLevel(logging.INFO)

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


varanus_logger.debug('This message should go to the log file')
varanus_logger.info('So should this')
varanus_logger.warning('And this, too')

t0 = time.time()
mon = Monitor("model/mascot-safety-system.csp", "event_map.json")
#mon.run_offline_rosmon("../rosmon-test/rosmon-mascot-pass.json")
#mon._run_offline_traces("trace.json")
mon._run_offline_traces_single("../mascot-test/scenario-traces/scenario1-trace.json")

#mon.run_online_traces_accumulate('127.0.0.1', 5090, timeRun=True)
#mon.run_online('127.0.0.1', 5044)
#mon.run_online_websocket('127.0.0.1', 8080)
mon.close()
t1 = time.time()

total = t1-t0
print("")
print("+++ Time: "+ str(total) +"s +++")
