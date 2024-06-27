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


PREVIEW_SCHEMA_ARGS = ["-p"]



def run_preview_schema_script(script_path: Path, output_path: Path = None) -> tuple[str, str]:
    process = subprocess.Popen(
        ['python', str(script_path)] + PREVIEW_SCHEMA_ARGS,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(CWD_PATH),
    )
    stdout, stderr = process.communicate()
    
    return stdout, stderr


pattern = r'.*Preview your schema at (.*?)\n'


def clear_output_dir():
    if DEFAULT_OUTPUT_PATH.exists():
        shutil.rmtree(DEFAULT_OUTPUT_PATH, ignore_errors=True)
    if CUSTOM_OUTPUT_PATH.exists():
        shutil.rmtree(CUSTOM_OUTPUT_PATH, ignore_errors=True) 

        
def get_output_path(stdout: str) -> Path:
    matches = re.findall(pattern, stdout)
    assert matches is not None
    return matches


def test_preview_single_module():
    clear_output_dir()
    stdout, stderr = run_preview_schema_script(SINGLE_MODULE_SCRIPT_PATH)
    
    assert stderr == ""

    matches = get_output_path(stdout)
    assert len(matches) == 1

    current_preview_url = matches[0]
    assert current_preview_url != ""
    
    assert "schemaKey=" in current_preview_url



def test_preview_multi_module():
    clear_output_dir()
    stdout, stderr = run_preview_schema_script(MULTI_MODULE_SCRIPT_PATH)
    
    assert stderr == ""
    matches = get_output_path(stdout)
    assert len(matches) == 1

    current_preview_url = matches[0]
    assert current_preview_url != ""
    
    assert "schemaKey=" in current_preview_url



def test_preview_addon_module():
    clear_output_dir()
    stdout, stderr = run_preview_schema_script(ADDON_SCRIPT_PATH)
    
    assert stderr == ""
    matches = get_output_path(stdout)
    assert len(matches) == 1

    current_preview_url = matches[0]
    assert current_preview_url != ""
    
    assert "schemaKey=" in current_preview_url
    
def test_preview_validator_module():
    clear_output_dir()
    stdout, stderr = run_preview_schema_script(VALIDATOR_SCRIPT_PATH)
    
    assert stderr == ""
    matches = get_output_path(stdout)
    assert len(matches) == 1

    current_preview_url = matches[0]
    assert current_preview_url != ""
    
    assert "schemaKey=" in current_preview_url

