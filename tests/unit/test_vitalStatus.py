import synapseclient
import pandas as pd
import mock
from nose.tools import assert_raises
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR,"../../processing"))

from vitalStatus import vitalStatus


def test_processing():
	syn = mock.create_autospec(synapseclient.Synapse) 

	vs = vitalStatus(syn, "SAGE")

	expectedvsDf = pd.DataFrame(dict(PATIENT_ID=["GENIE-SAGE-ID1","GENIE-SAGE-ID2","GENIE-SAGE-ID3","GENIE-SAGE-ID4","GENIE-SAGE-ID5"],
									 YEAR_DEATH=[1999,2000,3000,1000,1999],
									 YEAR_CONTACT=[1999,2000,3000,1000,1999],
									 INT_CONTACT=[1,2,3,4,3],
									 INT_DOD=[1,2,3,4,3],
									 DEAD=[True, False, True, False, True],
									 CENTER=["SAGE","SAGE","SAGE","SAGE","SAGE"]))

	vsDf = pd.DataFrame(dict(PATIENT_ID=["ID1","ID2","ID3","ID4","ID5"],
							 YEAR_DEATH=[1999,2000,3000,1000,1999],
							 YEAR_CONTACT=[1999,2000,3000,1000,1999],
							 INT_CONTACT=[1,2,3,4,3],
							 INT_DOD=[1,2,3,4,3],
							 DEAD=[True, False, True, False, True]))
	
	newvsDf = vs._process(vsDf)
	assert expectedvsDf.equals(newvsDf[expectedvsDf.columns])


def test_validation():
	syn = mock.create_autospec(synapseclient.Synapse) 

	vs = vitalStatus(syn, "SAGE")

	assert_raises(AssertionError, vs.validateFilename, ["foo"])
	assert vs.validateFilename(["vital_status.txt"]) == "vitalStatus"

	vsDf = pd.DataFrame(dict(PATIENT_ID=["ID1","ID2","ID3","ID4","ID5"],
							 YEAR_DEATH=[1999,2000,3000,1000,float('nan')],
							 YEAR_CONTACT=[1999,2000,3000,1000,1999],
							 INT_CONTACT=[1,2,3,4,3],
							 INT_DOD=[1,2,3,4,3],
							 DEAD=[True, False, True, False, True]))

	error, warning = vs.validate_helper(vsDf)
	assert error == ""
	assert warning == ""


	vsDf = pd.DataFrame()
	error, warning = vs.validate_helper(vsDf)
	expectedErrors = ("Vital status file: Must have PATIENT_ID column.\n"
					  "Vital status file: Must have YEAR_DEATH column.\n"
					  "Vital status file: Must have YEAR_CONTACT column.\n"
					  "Vital status file: Must have INT_CONTACT column.\n"
					  "Vital status file: Must have INT_DOD column.\n"
					  "Vital status file: Must have DEAD column.\n")
	assert error == expectedErrors
	assert warning == ""

	vsDf = pd.DataFrame(dict(PATIENT_ID=["ID1","ID2","ID3","ID4","ID5"],
							 YEAR_DEATH=[1999,2000,3000,3,float('nan')],
							 YEAR_CONTACT=[1999,2000,3000,2,1999],
							 INT_CONTACT=[1,2,3,4,float('nan')],
							 INT_DOD=[1,2,3,4,float('nan')],
							 DEAD=[True, False, True, float('nan'), True]))

	error, warning = vs.validate_helper(vsDf)
	expectedErrors = ("Vital status file: Please double check your YEAR_DEATH column, it must be an integer in YYYY format or NA/null/empty.\n"
					  "Vital status file: Please double check your YEAR_CONTACT column, it must be an integer in YYYY format.\n"
					  "Vital status file: Please double check your INT_CONTACT column, it must be an integer.\n"
					  "Vital status file: Please double check your INT_DOD column, it must be an integer.\n"
					  "Vital status file: Please double check your DEAD column, it must be a boolean value.\n")
	assert error == expectedErrors
	assert warning == ""