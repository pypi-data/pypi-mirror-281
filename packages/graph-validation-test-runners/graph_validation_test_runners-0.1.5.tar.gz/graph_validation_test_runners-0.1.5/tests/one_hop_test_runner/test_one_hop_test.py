"""
Unit tests for One Hop Test code validation
"""
import os
from sys import (
    # stdout,
    stderr
)
from typing import List, Dict
from json import dump
# import subprocess
import pytest

from graph_validation_tests.utils.unit_test_templates import (
    by_subject,
    inverse_by_new_subject,
    by_object,
    raise_subject_entity,
    raise_object_entity,
    raise_object_by_subject,
    raise_predicate_by_subject
)
from one_hop_test_runner import (
    OneHopTest,
    run_one_hop_tests
)
from tests import (
    # SCRIPTS_DIR,
    SAMPLE_MOLEPRO_INPUT_DATA,
    SAMPLE_ARAX_INPUT_DATA,
    SAMPLE_ARAGORN_INPUT_DATA,
    SAMPLE_JOINT_MOLEPRO_ARAX_INPUT_DATA,
    FULL_TEST
)


@pytest.mark.skipif(
    not FULL_TEST,
    reason="This test is a long running TRAPI query on active resources. Best not to run on CI!"
)
@pytest.mark.asyncio
async def test_one_hop_test():
    trapi_generators = [
        by_subject,
        inverse_by_new_subject,
        by_object,
        raise_subject_entity,
        raise_object_entity,
        raise_object_by_subject,
        raise_predicate_by_subject
    ]
    results: Dict = await OneHopTest.run_tests(
        **SAMPLE_MOLEPRO_INPUT_DATA,
        trapi_generators=trapi_generators,
        environment="ci",
        components=["aragorn", "molepro"]
    )
    dump(results, stderr, indent=4)


# ARS tests not yet supported so yes... results will
# always be empty, with a logger message to inform why
@pytest.mark.skipif(
    not FULL_TEST,
    reason="This test is a long running TRAPI query on active resources. Best not to run on CI!"
)
@pytest.mark.asyncio
async def test_one_hop_test_of_ars():
    trapi_generators = [
        by_subject,
        inverse_by_new_subject,
        by_object,
        raise_subject_entity,
        raise_object_entity,
        raise_object_by_subject,
        raise_predicate_by_subject
    ]
    results: Dict = await OneHopTest.run_tests(
        **SAMPLE_MOLEPRO_INPUT_DATA,
        trapi_generators=trapi_generators,
        environment="ci"
    )
    assert not results


@pytest.mark.parametrize(
    "data,environment,component,expected_result",
    [
        (
            SAMPLE_MOLEPRO_INPUT_DATA,
            "ci",
            "molepro",
            None
        ),
        (
            SAMPLE_ARAX_INPUT_DATA,
            "ci",
            "arax",
            None
        )
    ]
)
@pytest.mark.skipif(
    not FULL_TEST,
    reason="This test is a long running TRAPI query on active resources. Best not to run on CI!"
)
@pytest.mark.asyncio
async def test_run_one_hop_tests(
        data: Dict,
        environment: str,
        component: str,
        expected_result
):
    results: Dict = await run_one_hop_tests(
        **data,
        environment=environment,
        components=[component]
    )
    assert results
    dump(results, stderr, indent=4)


@pytest.mark.skipif(
    not FULL_TEST,
    reason="This test is a long running TRAPI query on active resources. Best not to run on CI!"
)
@pytest.mark.parametrize(
    "data,environment,components,expected_result",
    [
        (   # Query 0 - MolePro test
            SAMPLE_MOLEPRO_INPUT_DATA,
            "ci",
            ["molepro"],
            None
        ),
        (   # Query 1 - ARAX test
            SAMPLE_ARAX_INPUT_DATA,
            "ci",
            ["arax"],
            None
        ),
        (   # Query 2 - Aragorn test
            SAMPLE_ARAGORN_INPUT_DATA,
            "ci",
            ["aragorn"],
            None
        ),
        (   # Query 3 - Combined MolePro, ARAX and Aragorn test
            SAMPLE_MOLEPRO_INPUT_DATA,
            "ci",
            ["molepro", "arax", "aragorn"],
            None
        ),
        (   # Query 4 - Combined ARAX and MolePro test
            SAMPLE_JOINT_MOLEPRO_ARAX_INPUT_DATA,
            "ci",
            ["molepro", "arax"],
            None
        )
    ]
)
@pytest.mark.skipif(
    not FULL_TEST,
    reason="This test is a long running TRAPI query on active resources. Best not to run on CI!"
)
@pytest.mark.asyncio
async def test_run_one_hop_tests_with_runner_parameters(
        data: Dict,
        environment: str,
        components: List[str],
        expected_result
):
    results: Dict = await run_one_hop_tests(
        **data,
        environment=environment,
        components=components,
        strict_validation=True
    )
    assert results
    dump(results, stderr, indent=4)


# subprocess.run(
#     args, *, stdin=None, input=None, stdout=None, stderr=None,
#     capture_output=False, shell=False, cwd=None, timeout=None,
#     check=False, encoding=None, errors=None, text=None, env=None,
#     universal_newlines=None, **other_popen_kwargs
# )
# @pytest.mark.skip("Not yet fully implemented")
# def test_one_hop_cli():
#     # command: List = ["python", "-m", "one_hop_test_runner.__init__"]
#     # args: Dict = SAMPLE_TEST_INPUT_1.copy()
#     # args["components"] = "arax,molepro"
#     # [command.extend([f"--{flag}", value]) for flag, value in args.items()]
#     # results = check_output(["dir"])
#     # results = check_output([
#     #     "python", "-m", "venv", "--clear", "test_venv", ";",
#     #     ".", "test_venv/bin/activate"
#     # ])
#     subprocess.run("one_hop_test_runner", stdout=stdout, shell=True, cwd=SCRIPTS_DIR)
