from monitor import *

versionNum = 0.6
logging = True

print("+++++++++++++++++++++")
print("+++ VARANUS +++")
print("+++ version " + str(versionNum) + " +++")
print("+++ Matt Luckcuck +++")
print("+++++++++++++++++++++")



t0 = time.time()
mon = Monitor("model/mascot-safety-system.csp", "event_map.json")
#mon.run_offline_rosmon("../rosmon-test/rosmon-mascot-pass.json")
#mon._run_offline_traces("trace.json")
#mon._run_offline_traces_single("../mascot-test/scenario-traces/scenario1-trace.json")
mon.run_online_traces_accumulate('127.0.0.1', 5088)
#mon.run_online('127.0.0.1', 5044)
#mon.run_online_websocket('127.0.0.1', 8080)
mon.close()
t1 = time.time()

total = t1-t0
print("")
print("+++ Time: "+ str(total) +"s +++")
