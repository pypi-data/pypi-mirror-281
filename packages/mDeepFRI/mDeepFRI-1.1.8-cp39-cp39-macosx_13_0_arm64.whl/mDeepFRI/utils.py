import gzip
import json
import re
import shutil
import subprocess
import sys
import warnings
from glob import glob
from pathlib import Path
from typing import Dict, Iterable, List, Literal

import pysam
import requests
from pysam import FastaFile, FastxFile, tabix_compress


def run_command(command):
    """
    Runs a command and returns its output.

    Args:
        command (str): Command to run.
        timeout (int): Timeout in seconds.

    Returns:
        str: Command output.
    """

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True,
                               universal_newlines=True)

    stdout = []
    while True:
        line = process.stdout.readline()

        if not line:
            break
        stdout.append(line)
        print(line, end='')

    process.wait()
    if process.returncode != 0:
        raise RuntimeError(
            f"Command {command} failed with exit code {process.returncode}")

    # close file
    process.stdout.close()

    return "".join(stdout)


def download_file(url, path):
    """
    Downloads a file from url and saves it to path.

    Args:
        url (str): URL to download.
        path (str): Path to save the file.

    Returns:
        None
    """

    with requests.get(url, stream=True) as r:
        # check response and raise error
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(
                f"Download of {url} failed with error code {err.response.status_code}"
            ) from err

        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def download_model_weights(output_path: str,
                           version: Literal["1.0", "1.1"] = "1.1") -> None:
    """
    Downloads model weights and configs from the internet.

    Args:
        output_path (str): Path to save the files.

    Returns:
        None
    """
    from mDeepFRI import cnn_model_links, gcn_model_links

    output_path = Path(output_path)
    try:
        output_path.mkdir()
    except FileExistsError:
        # clean up the folder to avoid version conflicts
        shutil.rmtree(output_path)
        output_path.mkdir()

    for mode in gcn_model_links[version]:
        for url in gcn_model_links[version][mode].values():
            download_file(url, output_path / url.split("/")[-1])

    for mode in cnn_model_links:
        for url in cnn_model_links[mode].values():
            # version 1.1 does not perdict EC number
            if version == "1.1":
                if mode == "ec":
                    continue
            download_file(url, output_path / url.split("/")[-1])


def generate_config_json(weights_path: str, version: Literal["1.0",
                                                             "1.1"]) -> None:
    """
    Generates a config json file.

    Args:
        weights_path (str): Path to the weights folder.
        version (str): Version of the model.

    Returns:
        None
    """

    weights_path = Path(weights_path)
    config = {
        "gcn": {
            "bp": None,
            "cc": None,
            "mf": None,
            "ec": None
        },
        "cnn": {
            "bp": None,
            "cc": None,
            "mf": None,
            "ec": None
        },
        "version": None
    }

    models = list(weights_path.glob("*.onnx"))
    possible_modes = "|".join(list(config["cnn"].keys()))
    for model in models:
        mode = re.search(possible_modes, model.name).group(0)
        if "CNN" in model.name:
            config["cnn"][mode] = str(model)
        elif "GraphConv" in model.name:
            config["gcn"][mode] = str(model)

    config["version"] = version
    # version 1.1 doesn't predict EC
    if version == "1.1":
        del config["cnn"]["ec"]
        del config["gcn"]["ec"]

    config_name = "model_config.json"
    with open(weights_path / config_name, "w") as f:
        json.dump(config, f, indent=4, sort_keys=True)


def shutdown(message):
    """
    Terminates program execution with a reason.

    Args:
        message (str): Reason for termination.
    """
    sys.exit(message)


def remove_intermediate_files(temporary_files: Iterable):
    """
    Removes temporary files.

    Args:
        temporary_files (Iterable): List of temporary files.

    Returns:
        None
    """

    for file in temporary_files:
        extensions = glob(str(file) + "*")
        for ext in extensions:
            Path(ext).unlink()


def load_deepfri_config(weights: str) -> dict:
    """
    Check if DeepFRI weights are valid and load config.
    Args:
        weights: Path to DeepFRI weights.

    Returns:
        pathlib.Path: Path to DeepFRI config.
    """

    weights = Path(weights)
    assert weights.exists(), f"DeepFRI weights not found at {weights}"
    assert weights.is_dir(
    ), "DeepFRI weights should be a directory, not a file."

    config_path = weights / "model_config.json"
    assert config_path.exists(
    ), "DeepFRI weights are missing model_config.json"

    with open(config_path, "r", encoding="utf-8") as f:
        models_config = json.load(f)

    for net in ["cnn", "gcn"]:
        for model_type, model_path in models_config[net].items():
            model_name = weights / (Path(model_path).name)
            config_name = weights / (Path(model_path).stem +
                                     "_model_params.json")
            assert model_name.exists(
            ), f"DeepFRI weights are missing {model_type} model at {model_name}"
            assert config_name.exists(
            ), f"DeepFRI weights are missing {model_type} model config at {config_name}"
            # correct config
            models_config[net][model_type] = str(model_name.absolute())

    return models_config


def load_fasta_as_dict(fasta_file: str) -> Dict[str, str]:
    """
    Load FASTA file as dict of headers to sequences

    Args:
        fasta_file (str): Path to FASTA file. Can be compressed.

    Returns:
        Dict[str, str]: Dictionary of FASTA entries sorted by length.
    """

    with FastxFile(fasta_file) as fasta:
        fasta_dict = {entry.name: entry.sequence for entry in fasta}

    return fasta_dict


def retrieve_fasta_entries_as_dict(fasta_file: str,
                                   entries: List[str]) -> Dict[str, str]:
    """
    Retrieve selected FASTA entries as dict

    Args:
        fasta_file (str): Path to FASTA file. Can be compressed.
        entries (List[str]): List of entries to retrieve.

    Returns:
        Dict[str, str]: Dictionary of FASTA entries.
    """

    fasta_dict = dict()
    # silence pysam warnings for duplicate sequences
    verb = pysam.set_verbosity(0)

    try:
        fasta_handle = FastaFile(fasta_file)

    # catch gzipped files and recompress with bgzip
    except OSError:
        # unzip file
        with gzip.open(fasta_file, "rt") as f:
            content = f.read()
        # write to new file
        new_filepath = Path(fasta_file).parent / Path(fasta_file).stem
        with open(new_filepath, "w") as f:
            f.write(content)
            new_archive = str(new_filepath) + ".gz"
            tabix_compress(new_filepath, new_archive, force=True)
        fasta_handle = FastaFile(new_archive)

    with fasta_handle:
        for seq_id in entries:
            try:
                fasta_dict[seq_id] = fasta_handle.fetch(seq_id)
            except KeyError:
                raise ValueError(
                    f"Sequence with ID {seq_id} not found in {fasta_file}")

    # reset verbosity
    pysam.set_verbosity(verb)

    return fasta_dict


def stdout_warn(message, category, filename, lineno, file=None, line=None):
    sys.stdout.write(
        warnings.formatwarning(message, category, filename, lineno))
