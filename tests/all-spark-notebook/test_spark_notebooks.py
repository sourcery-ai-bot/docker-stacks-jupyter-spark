# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
from pathlib import Path

import pytest  # type: ignore

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.mark.parametrize(
    "test_file",
    # TODO: add local_sparklyr
    ["local_pyspark", "local_sparkR", "issue_1168"],
)
def test_nbconvert(container: TrackedContainer, test_file: str) -> None:
    """Check if Spark notebooks can be executed"""
    cont_data_dir = "/home/jovyan/data"
    output_dir = "/tmp"
    conversion_timeout_ms = 600
    host_data_dir = THIS_DIR / "data"
    LOGGER.info(f"Test that {test_file} notebook can be executed ...")
    command = (
        f"jupyter nbconvert --to markdown --ExecutePreprocessor.timeout={conversion_timeout_ms} "
        + f"--output-dir {output_dir} "
        + f"--execute {cont_data_dir}/{test_file}.ipynb"
    )
    logs = container.run_and_wait(
        timeout=60,
        volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
        tty=True,
        command=["start.sh", "bash", "-c", command],
    )

    expected_file = f"{output_dir}/{test_file}.md"
    assert expected_file in logs, f"Expected file {expected_file} not generated"
