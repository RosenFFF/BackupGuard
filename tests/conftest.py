import pytest
import os
from pathlib import Path

@pytest.fixture
def temp_dir(tmp_path):
    d = tmp_path / "test_root"
    d.mkdir()
    return d

@pytest.fixture
def dummy_file(temp_dir):
    f = temp_dir / "test.txt"
    f.write_text("dummy content")
    return f
