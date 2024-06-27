import pytest
import re
import shutil
import json
import subprocess
from pathlib import Path

examples_path = Path(__file__).parent.parent / "examples" / "task"

CWD_PATH = Path(__file__).parent

DEFAULT_OUTPUT_PATH = CWD_PATH / "generated_schemas"

CUSTOM_OUTPUT_PATH = CWD_PATH / "my_output_path"

SINGLE_MODULE_SCRIPT_PATH = examples_path / "cli.single.py"
MULTI_MODULE_SCRIPT_PATH = examples_path / "cli.multi.py"
ADDON_SCRIPT_PATH = examples_path / "cli.addon.py"
VALIDATOR_SCRIPT_PATH = examples_path / "cli.validator.py"


GEN_SCHEMA_ARGS_WITHOUT_OUTPUT = ["--gen-schema"]

EN_SCHEMA_ARGS_WITH_OUTPUT = ["--gen-schema", "--output"]


def run_gen_schema_script(script_path: Path, output_path: Path = None) -> tuple[str, str]:
    current_output_path = GEN_SCHEMA_ARGS_WITHOUT_OUTPUT if not output_path else EN_SCHEMA_ARGS_WITH_OUTPUT + [str(output_path)]
    process = subprocess.Popen(
        ['python', str(script_path)] + current_output_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(CWD_PATH),
    )
    stdout, stderr = process.communicate()
    
    return stdout, stderr

pattern = r'JSONSchema describe file for .*? has been generated successfully to (.*?)\n'

def clear_output_dir():
    if DEFAULT_OUTPUT_PATH.exists():
        shutil.rmtree(DEFAULT_OUTPUT_PATH, ignore_errors=True)
    if CUSTOM_OUTPUT_PATH.exists():
        shutil.rmtree(CUSTOM_OUTPUT_PATH, ignore_errors=True) 

        
def get_output_path(stdout: str) -> Path:
    matches = re.findall(pattern, stdout)
    assert matches is not None
    return matches

def test_gen_single_module():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(SINGLE_MODULE_SCRIPT_PATH)
    
    assert stderr == ""

    matches = get_output_path(stdout)
    assert len(matches) == 1
    current_output_path: Path = CWD_PATH / matches[0]
    assert current_output_path.exists()

    content = current_output_path.read_text()
    assert content != ""
    res = json.loads(content)
    assert type(res) == dict
    assert res.get("model_type") == "single"
    
def test_gen_single_module_with_output():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(SINGLE_MODULE_SCRIPT_PATH, CUSTOM_OUTPUT_PATH)
    
    assert stderr == ""
    assert CUSTOM_OUTPUT_PATH.exists()

    matches = get_output_path(stdout)
    
    assert len(matches) == 1
    current_output_path: Path = CUSTOM_OUTPUT_PATH / matches[0]
    assert current_output_path.exists()
    assert current_output_path.is_relative_to(CUSTOM_OUTPUT_PATH)
    
    content = current_output_path.read_text()
    assert content != ""
    res = json.loads(content)
    assert type(res) == dict
    assert res.get("model_type") == "single"
    
    
def test_gen_multi_module():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(MULTI_MODULE_SCRIPT_PATH)
    
    assert stderr == ""
    matches = get_output_path(stdout)
    assert len(matches) > 1
    
    for match in matches:
        current_output_path = CWD_PATH / Path(match)
        assert current_output_path.exists()

        content = current_output_path.read_text()
        assert content != ""
        res = json.loads(content)
        assert type(res) == dict
        assert res.get("model_type") == "multiple"

def test_gen_multi_module_with_output():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(MULTI_MODULE_SCRIPT_PATH, CUSTOM_OUTPUT_PATH)
    
    assert stderr == ""
    assert CUSTOM_OUTPUT_PATH.exists()

    matches = get_output_path(stdout)
    assert len(matches) > 1
    
    for match in matches:
        current_output_path = CUSTOM_OUTPUT_PATH / Path(match)
        assert current_output_path.exists()
        assert current_output_path.is_relative_to(CUSTOM_OUTPUT_PATH)

        content = current_output_path.read_text()
        assert content != ""
        res = json.loads(content)
        assert type(res) == dict
        assert res.get("model_type") == "multiple"



def test_gen_addon_module():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(ADDON_SCRIPT_PATH)
    
    assert stderr == ""
    matches = get_output_path(stdout)
    assert len(matches) == 1
    
    current_output_path: Path = CWD_PATH / matches[0]
    assert current_output_path.exists()

    content = current_output_path.read_text()
    assert content != ""
    res = json.loads(content)
    assert type(res) == dict
    
def test_gen_addon_module_with_output():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(ADDON_SCRIPT_PATH, CUSTOM_OUTPUT_PATH)
    
    assert stderr == ""
    assert CUSTOM_OUTPUT_PATH.exists()

    matches = get_output_path(stdout)
    assert len(matches) == 1
    
    current_output_path: Path = CUSTOM_OUTPUT_PATH / matches[0]
    assert current_output_path.exists()
    assert current_output_path.is_relative_to(CUSTOM_OUTPUT_PATH)

    content = current_output_path.read_text()
    assert content != ""
    res = json.loads(content)
    assert type(res) == dict


def test_gen_validator_module():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(VALIDATOR_SCRIPT_PATH)
    
    assert stderr == ""
    matches = get_output_path(stdout)
    assert len(matches) == 1
    
    current_output_path: Path = CWD_PATH / matches[0]
    assert current_output_path.exists()

    content = current_output_path.read_text()
    assert content != ""
    res = json.loads(content)
    assert type(res) == dict
    
def test_gen_validator_module_with_output():
    clear_output_dir()
    stdout, stderr = run_gen_schema_script(VALIDATOR_SCRIPT_PATH, CUSTOM_OUTPUT_PATH)
    
    assert stderr == ""
    assert CUSTOM_OUTPUT_PATH.exists()

    matches = get_output_path(stdout)
    assert len(matches) == 1
    
    current_output_path: Path = CUSTOM_OUTPUT_PATH / matches[0]
    assert current_output_path.exists()
    assert current_output_path.is_relative_to(CUSTOM_OUTPUT_PATH)

    content = current_output_path.read_text()
    assert content != ""
    res = json.loads(content)
    assert type(res) == dict
