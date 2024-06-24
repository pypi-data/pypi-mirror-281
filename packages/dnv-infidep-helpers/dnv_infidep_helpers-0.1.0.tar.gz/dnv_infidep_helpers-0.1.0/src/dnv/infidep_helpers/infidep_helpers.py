"""
Helper functions to run Infidep on the OneWorkflow platform.

OneWorkflow is a DNV platform that allow computational workflows to be
built and run locally or in the cloud. It is a generic system, so there are
several configuration options.

The methods in this module hide the complexity for users who just want to run
Infidep calculations and soil spring calibrations.
"""
from glob import glob
import json
from os import PathLike, makedirs, path
from pathlib import Path
import shutil
from typing import List, Union
import uuid
import tempfile
import os
from dnv.onecompute import Environment, WorkStatus
from dnv.onecompute.file_service import FileTransferOptions
from dnv.oneworkflow import ParallelWork
from dnv.oneworkflow.utils import run_managed_commands_in_parallel_async
from dnv.oneworkflow.utils.command_info import CommandInfo
from dnv.oneworkflow.utils.one_workflow_client_builder import (
    one_workflow_client
)
from dnv.oneworkflow.utils.workflow_runners_managed import (
    run_managed_workflow_async
)
from dnv.sesam.commands.infidep_calibration_command import (
    CalibrationCommand
)
from dnv.sesam.commands.infidep_work_unit import create_infidep_work_unit
from dnv.oneworkflow.oneworkflowclient import OneWorkflowClient

COMMONFILES_DIR = "CommonFiles"
LOADCASES_DIR = "LoadCases"
INPUT_FILE_NAME = "input.json"
RESULTS_FILE_NAME = "results.json"


def _create_infidep_client(workspace_path: PathLike[str]) -> OneWorkflowClient:
    return one_workflow_client(
        workspace_id=workspace_path.name,
        workspace_path=str(workspace_path),
        cloud_run=True,
        application_id='Infidep',
        environment=Environment.Testing,
        pool_id='Kubernetes.tstk8stasks'
    )


def _create_calibration_client(
        workspace_path: PathLike[str]
        ) -> OneWorkflowClient:
    return one_workflow_client(
        workspace_id=workspace_path.name,
        workspace_path=str(workspace_path),
        application_id="OneWorkflowWorkerWindows",
        executable_name="OneWorkflowWorkerHost",
        environment=Environment.Testing,
        pool_id="InfidepCalibration",
        cloud_run=True
    )


def _create_workspace(input_data: Union[dict, List[dict]]) -> Path:

    if not isinstance(input_data, list):
        input_data = [input_data]

    workspace_id = uuid.uuid4()
    temp_dir = Path(tempfile.gettempdir())
    workspace_dir = temp_dir.joinpath(f"workspace_{workspace_id}")

    makedirs(workspace_dir.joinpath(COMMONFILES_DIR))

    loadcases_dir = workspace_dir.joinpath(LOADCASES_DIR)
    makedirs(loadcases_dir)

    loadcase_count = 0

    for loadcase_input in input_data:
        loadcase = f'LoadCase{loadcase_count:05d}'
        loadcase_count += 1
        loadcase_dir = loadcases_dir.joinpath(loadcase)
        makedirs(loadcase_dir)
        with open(
                loadcase_dir.joinpath(INPUT_FILE_NAME),
                "w",
                encoding="utf8") as f:
            f.write(json.dumps(loadcase_input))

    return workspace_dir


def _load_json_from_file(json_file: Path) -> dict:
    with open(json_file, "r", encoding="utf8") as f:
        return json.load(f)


def _read_results(
        workspace_path: Path,
        results_file_name: str = RESULTS_FILE_NAME) -> List[dict]:
    loadcases_dir = workspace_path.joinpath(LOADCASES_DIR)
    files = glob(f'LoadCase*/{results_file_name}', root_dir=loadcases_dir)
    sorted_files = sorted(files)
    results_files = list(map(loadcases_dir.joinpath, sorted_files))
    return list(map(_load_json_from_file, results_files))


def _loadcase_name(loadcase_dir: Path) -> str:
    loadcase_name = loadcase_dir.name
    if loadcase_dir.joinpath(INPUT_FILE_NAME).exists():
        input_data = _load_json_from_file(
            loadcase_dir.joinpath(INPUT_FILE_NAME))
        if 'project_id' in input_data.keys():
            loadcase_name = input_data['project_id']
    return loadcase_name


def _copy_result_files(
        workspace_path: Path,
        destination_dir: Path):
    """
    Copy the input and results files from the loadcase directory to 
    a directory of the user's choice. If the destination directory is
    not provided, the files will be copied to a Results directory below
    the current directory.

    The individual results folders will be named after the project_id, if 
    available. If there is already a directory with that name, a number will
    be appended to avoid overwriting previous results.
    """
    for d in [subdir
              for subdir
              in workspace_path.joinpath(LOADCASES_DIR).iterdir()
              if subdir.is_dir()]:
        loadcase_name = _loadcase_name(d)
        loadcase_destination = destination_dir.joinpath(loadcase_name)
        if loadcase_destination.exists():
            dupe_count = 0
            while loadcase_destination.exists():
                dupe_count += 1
                loadcase_destination = destination_dir.joinpath(
                    f'{loadcase_name}_{dupe_count}')

        shutil.copytree(d, loadcase_destination,
                        ignore=shutil.ignore_patterns('std*.txt'))

    print(f'Results have been stored in {destination_dir}')


def _read_and_validate_results(
        workspace_path: Path,
        input_data: Union[dict, List[dict]]) -> Union[dict, List[dict]]:

    results = _read_results(workspace_path)

    if isinstance(input_data, list):
        if len(results) != len(input_data):
            raise ValueError(
                f"Incorrect number of results. Expected {len(input_data)} "
                f"got {len(results)}")
    else:
        # The user passed in a single input_data, not a list
        results = results[0]

    return results


def _create_results_dir(results_dir: Union[str, Path]) -> Path:
    """
    Try to create the results directory
    """
    if not results_dir:
        results_dir = Path(os.getcwd()).joinpath("Results")

    results_dir = (results_dir
                   if isinstance(results_dir, Path)
                   else Path(results_dir))
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


async def run_infidep_async(
        input_data: Union[dict, List[dict]],
        results_dir: Union[str, os.PathLike] = None) -> Union[dict, List[dict]]:
    """
    Runs an Infidep calculation in the cloud.

    You may be prompted to sign in to OneCompute when you run this method. The 
    calculation is run using the input_data, and the results are returned. The
    input and result files are also saved in the results_dir.

    The input data can either be a single dictionary, or a list of dictionaries,
    which will run several calculations in parallel. The results will be a single
    dictionary for a single calculation, or a list of dictionaries for multiple 
    calculations.

    Keyword arguments:
    input_data -- The input data for the calculation.
    results_dir -- The location to store the result file. If not supplied, this
        defaults to a "Results" directory below the working directory.
    """

    results_dir = _create_results_dir(results_dir)

    workspace = _create_workspace(input_data)
    client = _create_infidep_client(workspace)
    work_units = []
    for load_case in workspace.joinpath(LOADCASES_DIR).iterdir():
        if path.isdir(load_case):
            work_units.append(
                create_infidep_work_unit(
                    client,
                    load_case.name,
                    infidep_version='demo8'))

    work = work_units[0] if len(work_units) == 1 else ParallelWork(work_units)
    result = await run_managed_workflow_async(
        client,
        work,
        files_to_upload_from_client_to_blob=FileTransferOptions(
            patterns=[f"**/{INPUT_FILE_NAME}"]),
        files_to_download_from_blob_to_client=FileTransferOptions(
            patterns=["**/results.json"])
    )

    if result.job_info.Status != WorkStatus.Completed:
        raise ValueError(
            f"Unexpected result: {result.job_info.Status}. "
            f"The job ID for support is {result.job_info.JobId}")

    results = _read_and_validate_results(workspace, input_data)
    _copy_result_files(workspace, results_dir)

    client.delete_workspace_container()
    shutil.rmtree(workspace)

    return results


async def run_infidep_splice_calibration_async(
        input_data: Union[dict, List[dict]],
        results_dir: Union[str, Path] = None,
        quick_mode: bool = False) -> Union[dict, List[dict]]:
    """
    Runs an Infidep/Splice calibration in the cloud.

    You may be prompted to sign in to OneCompute when you run this method. The
    calibration is run using the input_data, and the results are returned. The
    input and result files are also saved in the results_dir.

    The input data can either be a single dictionary, or a list of dictionaries,
    which will run several calibrations in parallel. The results will be a single
    dictionary for a single calibrations, or a list of dictionaries for multiple
    calibrations.

    Keyword arguments:
    input_data -- The input data for the calibration.
    results_dir -- The location to store the result file. If not supplied, this
        defaults to a "Results" directory below the working directory.
    """
    results_dir = _create_results_dir(results_dir)
    workspace = _create_workspace(input_data)
    client = _create_calibration_client(workspace)

    commands_info = []
    for load_case in workspace.joinpath(client.load_cases_directory).iterdir():
        if path.isdir(load_case):
            command = CalibrationCommand(
                input_file_name=INPUT_FILE_NAME,
                quick_mode=quick_mode
            )

        commands_info.append(CommandInfo(
            commands=[command],
            load_case_foldername=load_case.name
        ))

    await run_managed_commands_in_parallel_async(client, commands_info)

    results = _read_and_validate_results(workspace, input_data)
    _copy_result_files(workspace, results_dir)
    client.delete_workspace_container()
    shutil.rmtree(workspace)

    return results
