# mascot-test
### Matt Luckcuck
### 2020-07-07 Varanus v0.88

Various test traces for the MASCOT system, and two 'dummy' MASCOTs that just send events from a given trace file to Varanus. `dummy_mascot_socket.py` sends the events down a socket, and predictably, `dummy_mascot_websocket.py` sends  events using websockets.

The `dummy_mascot_ifm.py` file is the version used in the paper "Monitoring Robotic Systems using CSP: From Safety Designs to Safety Monitors" (which is in the `varanus/papers` directory) and the `scenario-traces` directory contains the traces for the stress-tests scenarios and mission scenarios used in the paper.

## Usage

To run the examples for the the paper "Monitoring Robotic Systems using CSP: From Safety Designs to Safety Monitors", you will need two terminal windows open in the `varanus` root directory (or one each in the `varanus-python` and `mascot-test` directories, respectively).

### Basic Usage

The files are setup to run online RV using Scenario 1 over a localhost socket.

1. In one terminal, we run the Dummy MASCOT `python mascot-test/dummy_mascot_socket_ifm.py`. It should wait, listening for Varanus to connect, before it starts sending events.
2. In the other terminal, we start Varanus `python varanus-python/varanus.py`. It should connect to the Dummy MASCOT and receive events, which you should see via the terminal being checked in FDR.

### Running Other Scenarios

To run the other scenarios, you need to alter some of the parameters in the two files we used in **Basic Usage**.

* In `python mascot-test/dummy_mascot_socket_ifm.py` edit the `FILE` constant to point at the scenario trace you want to use (they can be found in the `mascot-test/scenario-traces` directory).
* In `python varanus-python/varanus.py` edit the `logFileName` to match the scenario you've picked (this is more so that the logs match rather than for any functional reason).

### Running Varanus for Offline RV

To run Varanus for Offline RV, we only need one terminal open in the `varanus/varanus-python`  directory.

1. Edit the `varanus.py` file.
Change this:
```python
#mon._run_offline_traces_single("../mascot-test/scenario-traces/scenario1-trace.json")
mon.run_online_traces_accumulate('127.0.0.1', 5088, timeRun=True)
```
to this:
```python
mon._run_offline_traces_single("../mascot-test/scenario-traces/scenario1-trace.json")
#mon.run_online_traces_accumulate('127.0.0.1', 5088, timeRun=True)
```
2. Run Varanus `python varanus.py`. It should read the trace from the file (in this case, scenario 1) and check it against the model.

To check other scenarios offline, edit the parameter passed to `_run_offline_traces_single()` to point at one of the other files in `varanus//mascot-test/scenario-traces`.
