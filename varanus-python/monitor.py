from fdr_interface import FDRInterface

#"MASCOT_SAFETY_SYSTEM :[has trace]: <system_init>""
#"csp/mascot-safety-system.csp


fdr = FDRInterface()

fdr.load_model("model/mascot-safety-system.csp")

print fdr.check_trace(["system_init"])

fdr.close()
