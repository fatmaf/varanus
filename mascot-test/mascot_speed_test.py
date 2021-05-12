import json
import time
import csv
import os
import sys
import time
import subprocess
sys.path.append("../varanus-python/")
import fdr_interface
import trace_representation
import fdr




##CONSTANTS###
MODEL = "../varanus-python/model/mascot-safety-system.csp"
TRACES_DIR = "scenario-traces/"
API_OUTPUT_DIR = "api-times/"
OFFLINE_OUTPUT_DIR = "offline-times/"
ONLINE_OUTPUT_DIR =  "online-times/"
SOURCE_LIST = ["scenario1-trace", "scenario2-trace", "scenario2a-trace", "scenario2b-trace",
"scenario3-trace", "scenario4-trace", "scenario4a-trace", "scenario4b-trace", "scenario5-trace",
"scenario6-trace", "scenario7-trace", "scenario0-10-trace", "scenario0-100-trace", "scenario0-1000-trace",
"scenario0-10000-trace", "scenario0-100000-trace"]
###


#Adapted from middle of far_interface._make_assertion()
def _make_assertion(trace):
    #generate assert and dump it into the model
    assert_start = "MASCOT_SAFETY_SYSTEM  :[has trace]: <"
    assert_end = ">"

    assert_check = assert_start
    trace_list = trace


    for i in range(len(trace_list)):
        # the str is key here. My editor produced unicode which became
        # a unicode object, not a str object so the assertion parsing broke.
        event = str(trace_list[i])

        assert_check = assert_check + event
        if i < len(trace_list)-1:
            assert_check = assert_check + ", "
        elif i == len(trace_list)-1:
            assert_check = assert_check + assert_end

    return assert_check

def write_csv(scenario_name, times_list, output_dir):
    """ Output the times_list to a csv (with a name containing the scenario_name)
    with a mean average of the times """

    print(scenario_name, times_list)
    output_file = open(output_dir+scenario_name+".csv", "w")

    csv_write = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_write.writerow(['Name', 'Time (s)'])
    run_num = 0
    sumOfNumbers = 0
    for time in times_list:
        run_num += 1
        sumOfNumbers = sumOfNumbers + time
        csv_write.writerow([ "Run" + str(run_num) , time ])


    mean = sumOfNumbers / len(times_list)

    csv_write.writerow(['Mean', mean])
    output_file.close()



def api_time_check():

    fdr.library_init()

    for scenario_name in SOURCE_LIST[0:2]:
        print ("SCENARIO:" + scenario_name)
        times = []

        file_name = TRACES_DIR + scenario_name + ".json"
        trace_file = open(file_name)
        trace_line = trace_file.read()
        # parse to list
        event_list =json.loads(trace_line)

        assertion_text = _make_assertion(event_list)

        # do the check ten times
        for i in range(10):
            #Prep
            print("before library_init()")

            session = fdr.Session()
            session.load_file(MODEL)

            parsedAssert = session.parse_assertion(assertion_text)
            assertion = parsedAssert.result()

            t0 = time.time()
            #CHECK
            assertion.execute(None)
            t1 = time.time()

            print "%s: %s" % (assertion, "Passed" if assertion.passed() else "Failed")


            total = t1-t0
            times.append(total)
            print(total)


        write_csv(scenario_name, times, API_OUTPUT_DIR)

    fdr.library_exit()

def offline_time_check():

    for scenario_name in SOURCE_LIST[0:1]:
        print("+++ SCENARIO " + scenario_name + " +++")
        print("")
        for i in range(10):
            print("+++ RUN NUMBER " + str(i+1) + " +++")
            print("")
            os.system("python ../varanus-python/varanus.py ../varanus-python/model/mascot-safety-system.csp ../varanus-python/event_map.json offline -n" + scenario_name + " --log_path='../mascot-test/offline-times' -t ../mascot-test/scenario-traces/" + scenario_name + ".json" )
            time.sleep(1)

def online_time_check():



    for scenario_name in SOURCE_LIST[0:1]:
        subprocess.call("python dummy_mascot_speed_check.py scenario-traces/" + scenario_name + ".json")
        print("+++ SCENARIO " + scenario_name + " +++")
        print("")
        for i in range(2):
            print("+++ RUN NUMBER " + str(i+1) + " +++")
            print("")


            os.system("python ../varanus-python/varanus.py ../varanus-python/model/mascot-safety-system.csp ../varanus-python/event_map.json online -n" + scenario_name + " --log_path='../mascot-test/online-times' ")
            time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    #api_time_check()
    #offline_time_check()
    online_time_check()
