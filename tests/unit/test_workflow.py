import synapseclient
import pandas as pd
import mock
from nose.tools import assert_raises
import os
import sys
from genie.workflow import workflow

def test_processing():

    syn = mock.create_autospec(synapseclient.Synapse) 

    workflowClass = workflow(syn, "SAGE")
    pass

def test_validation():

    syn = mock.create_autospec(synapseclient.Synapse) 

    workflowClass = workflow(syn, "SAGE")

    assert_raises(AssertionError, workflowClass.validateFilename, ["foo"])
    assert_raises(AssertionError, workflowClass.validateFilename, ["SAGE-test.txt"])
    assert workflowClass.validateFilename(["SAGE-test.md"]) == "md"
