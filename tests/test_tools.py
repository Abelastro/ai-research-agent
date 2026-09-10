import pytest
import os
import tempfile
from src.tools.calculator import calculator
from src.tools.web_search import web_search
from src.tools.data_analysis import data_analysis
from src.tools.file_reader import read_file, read_csv, list_directory
from src.tools.code_analyzer import analyze_python_code, extract_imports, count_complexity


@pytest.mark.asyncio
async def test_calculator_basic():
    result = await calculator(expression="2 + 3 * 4")
    assert "14" in result


@pytest.mark.asyncio
async def test_calculator_invalid_expression():
    result = await calculator(expression="1/0")
    assert "Error" in result


@pytest.mark.asyncio
async def test_calculator_security():
    result = await calculator(expression="__import__('os').system('ls')")
    assert "Error" in result or "invalid" in result.lower()


@pytest.mark.asyncio
async def test_data_analysis_with_csv():
    csv_data = "x,y\n1,2\n3,4\n5,6"
    result = await data_analysis(query="analyze", csv_data=csv_data)
    assert "Data Analysis" in result
    assert "Shape" in result


@pytest.mark.asyncio
async def test_data_analysis_no_data():
    result = await data_analysis(query="analyze")
    assert "No data source" in result


@pytest.mark.asyncio
async def test_web_search_returns_result():
    result = await web_search(query="test")
    assert "Search results" in result
    assert "test" in result


@pytest.mark.asyncio
async def test_file_reader():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("hello world\nline 2")
        temp_path = f.name
    try:
        result = await read_file(temp_path)
        assert "hello world" in result
        assert "line 2" in result
    finally:
        os.unlink(temp_path)


@pytest.mark.asyncio
async def test_code_analyzer():
    code = """
import os
import sys

def hello():
    return "hi"

class Foo:
    pass
"""
    result = await analyze_python_code(code)
    assert "Functions" in result
    assert "hello" in result
    assert "Classes" in result
    assert "Foo" in result


@pytest.mark.asyncio
async def test_extract_imports():
    code = "import os\nfrom sys import argv"
    result = await extract_imports(code)
    assert "os" in result


@pytest.mark.asyncio
async def test_count_complexity():
    code = "if True:\n    if False:\n        pass"
    result = await count_complexity(code)
    assert result >= 2


@pytest.mark.asyncio
async def test_list_directory():
    result = await list_directory(os.path.dirname(__file__))
    assert "Directory" in result


@pytest.mark.asyncio
async def test_read_csv():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("a,b\n1,2\n3,4")
        temp_path = f.name
    try:
        result = await read_csv(temp_path)
        assert "CSV File" in result
        assert "Shape" in result
    finally:
        os.unlink(temp_path)
