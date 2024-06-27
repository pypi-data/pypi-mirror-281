import pytest
import re
import shutil
import json
import subprocess
from pathlib import Path

examples_path = Path(__file__).parent.parent / "examples" / "task"
test_data_path = Path(__file__).parent / "data"
CWD_PATH = Path(__file__).parent

SINGLE_MODULE_SCRIPT_PATH = examples_path / "cli.single.py"
TEST_DATA_SINGLE_MODULE_PATH = test_data_path / "test.single.json"

MULTI_MODULE_SCRIPT_PATH = examples_path / "cli.multi.py"
TEST_DATA_MULTI_MODULE_GBSA_PATH = test_data_path / "test.multi_gbsa.json"
TEST_DATA_MULTI_MODULE_SCAN_PATH = test_data_path / "test.multi_scan.json"


ADDON_SCRIPT_PATH = examples_path / "cli.addon.py"
TEST_DATA_ADDON_PATH = test_data_path / "test.addon.json"

VALIDATOR_SCRIPT_PATH = examples_path / "cli.validator.py"
TEST_DATA_VALIDATOR_FAILED_PATH = test_data_path / "test.validator_failed.json"
TEST_DATA_VALIDATOR_SUCCESS_PATH = test_data_path / "test.validator_success.json"


RUN_TYPING_ARGS = ["--json-config"]

def run_typing_cli_script(script_path: Path, test_data_path: Path, model_name: str = None) -> tuple[str, str, int]:
    current_args = [model_name] + RUN_TYPING_ARGS + [str(test_data_path)] if model_name else RUN_TYPING_ARGS + [str(test_data_path)]
    process = subprocess.Popen(
        ['python', str(script_path)] + current_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=CWD_PATH
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode



def test_exec_single_module():
    stdout, stderr, exit_code = run_typing_cli_script(
        SINGLE_MODULE_SCRIPT_PATH,
        TEST_DATA_SINGLE_MODULE_PATH,
    )
    
    assert stderr == ""
    assert exit_code == 0
    assert stdout != ""
    
def test_exec_multi_module():
    stdout, stderr, exit_code = run_typing_cli_script(
        MULTI_MODULE_SCRIPT_PATH,
        TEST_DATA_MULTI_MODULE_GBSA_PATH,
        "gbsa"
    )
    
    assert stderr == ""
    assert exit_code == 0
    assert stdout != ""
    
    stdout, stderr, exit_code = run_typing_cli_script(
        MULTI_MODULE_SCRIPT_PATH,
        TEST_DATA_MULTI_MODULE_SCAN_PATH,
        "scan"
    )
    
    assert stderr == ""
    assert exit_code == 0
    assert stdout != ""


def test_exec_addon():
    stdout, stderr, exit_code = run_typing_cli_script(
        ADDON_SCRIPT_PATH,
        TEST_DATA_ADDON_PATH,
    )
    
    assert stderr == ""
    assert exit_code == 0
    assert stdout != ""


def test_exec_validator():
    stdout, stderr, exit_code = run_typing_cli_script(
        VALIDATOR_SCRIPT_PATH,
        TEST_DATA_VALIDATOR_FAILED_PATH,
    )
    
    assert stderr != ""
    assert exit_code == 1
    
    stdout, stderr, exit_code = run_typing_cli_script(
        VALIDATOR_SCRIPT_PATH,
        TEST_DATA_VALIDATOR_SUCCESS_PATH,
    )
    assert stderr == ""
    assert exit_code == 0
    assert stdout != ""

