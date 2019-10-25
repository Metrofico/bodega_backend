import errno
import io
import json
import os
import platform
import shlex
import subprocess
from logging import getLogger

import numpy as np
import pandas as pd

from .errors import CSVParseError, JavaNotFoundError
from .file_util import localize_file
from .template import load_template
from .util import deprecated_option

logger = getLogger(__name__)

TABULA_JAVA_VERSION = "1.0.4"
JAR_NAME_WITH_DEPENDENCIES = "tabula-{}-jar-with-dependencies.jar".format(TABULA_JAVA_VERSION)
JAR_NAME = "tabula-{}.jar".format(TABULA_JAVA_VERSION)
JAR_MAIN_CLASS = "technology.tabula.CommandLineApp"
JAR_DIR = os.path.abspath(os.path.dirname(__file__))
JAVA_NOT_FOUND_ERROR = (
    "El comando `java` no se encontro ."
    "Por favor asegurese de que JAVA esta instalado y ha establecido el PATH de `java`"
)

DEFAULT_CONFIG = {"JAR_PATH": os.path.join(JAR_DIR, JAR_NAME)}


def _jar_path():
    return os.environ.get("TABULA_JAR", DEFAULT_CONFIG["JAR_PATH"])


def _jar_patch_with_dependencies():
    # -classpath "$SERVICE:lib/*" net.md_5.bungee.Bootstrap
    return DEFAULT_CONFIG["JAR_PATH"] + ";" + JAR_DIR + "/lib" + "/*"


def _jar_main_class():
    return JAR_MAIN_CLASS


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
    output_all = ""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            INFO = str(output, "utf8")
            if "@[CSVWriterEND]" in INFO:
                break;
            if "@[JSONWriterEND]" in INFO:
                break;
            if "[PROGRESS]" in INFO:
                print("", INFO.replace("[PROGRESS]", "").strip())
            else:
                output_all += str(output, "utf8")
    return str(output_all).encode("utf-8")


def _run(java_options, options, path=None, encoding="utf-8"):
    """Call tabula-java with the given lists of Java options and tabula_py
    options, as well as an optional path to pass to tabula-java as a regular
    argument and an optional encoding to use for any required output sent to
    stderr.

    tabula_py options are translated into tabula-java options, see
    :func:`build_options` for more information.
    """
    # Workaround to enforce the silent option. See:
    # https://github.com/tabulapdf/tabula-java/issues/231#issuecomment-397281157
    if "silent" in options:
        java_options.extend(
            (
                "-Dorg.slf4j.simpleLogger.defaultLogLevel=off",
                "-Dorg.apache.commons.logging.Log"
                "=org.apache.commons.logging.impl.NoOpLog",
            )
        )

    built_options = build_options(options)
    args = ["java"] + java_options + ["-cp", _jar_patch_with_dependencies(), _jar_main_class()] + built_options
    if path:
        args.append(path)

    try:
        comando = ""
        for flag in args:
            comando += flag + " "

        print("Argumento " + str(comando))
        output = run_command(args)
        # output = subprocess.check_output(args)
        return output
    except FileNotFoundError:
        raise JavaNotFoundError(JAVA_NOT_FOUND_ERROR)
    except subprocess.CalledProcessError as e:
        logger.error("Error encontrado: {}\n".format(e.output.decode(encoding)))
        raise


def read_pdf(
        input_path,
        output_format="dataframe",
        encoding="utf-8",
        java_options=None,
        pandas_options=None,
        multiple_tables=False,
        user_agent=None,
        **kwargs
):
    if output_format == "dataframe":
        kwargs.pop("format", None)

    elif output_format == "json":
        kwargs["format"] = "JSON"

    if multiple_tables:
        kwargs["format"] = "JSON"

    if java_options is None:
        java_options = []

    elif isinstance(java_options, str):
        java_options = shlex.split(java_options)

    # to prevent tabula_py from stealing focus on every call on mac
    if platform.system() == "Darwin":
        if not any("java.awt.headless" in opt for opt in java_options):
            java_options += ["-Djava.awt.headless=true"]

    if encoding == "utf-8":
        if not any("file.encoding" in opt for opt in java_options):
            java_options += ["-Dfile.encoding=UTF8"]

    path, temporary = localize_file(input_path, user_agent)

    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    if os.path.getsize(path) == 0:
        raise ValueError(
            "{} is empty. Check the file, or download it manually.".format(path)
        )

    try:
        output = _run(java_options, kwargs, path, encoding)
    finally:
        if temporary:
            os.unlink(path)

    if len(output) == 0:
        logger.warning("The output file is empty.")
        return

    if pandas_options is None:
        pandas_options = {}

    fmt = kwargs.get("format")
    if fmt == "JSON":
        raw_json = json.loads(output.decode(encoding))
        if multiple_tables:
            return _extract_from(raw_json, pandas_options)

        else:
            return raw_json

    else:
        pandas_options["encoding"] = pandas_options.get("encoding", encoding)

        try:
            return pd.read_csv(io.BytesIO(output), **pandas_options)

        except pd.errors.ParserError as e:
            message = "Error failed to create DataFrame with different column tables.\n"
            message += (
                "Try to set `multiple_tables=True`"
                "or set `names` option for `pandas_options`. \n"
            )

            raise CSVParseError(message, e)


def read_pdf_with_template(
        input_path,
        template_path,
        pandas_options=None,
        encoding="utf-8",
        java_options=None,
        user_agent=None,
        **kwargs
):
    path, temporary = localize_file(
        template_path, user_agent=user_agent, suffix=".json"
    )
    options = load_template(path)
    dataframes = []

    try:
        for option in options:
            _df = read_pdf(
                input_path,
                pandas_options=pandas_options,
                encoding=encoding,
                java_options=java_options,
                **dict(kwargs, **option)
            )

            if isinstance(_df, list):
                dataframes.extend(_df)
            else:
                dataframes.append(_df)
    finally:
        if temporary:
            os.unlink(path)

    return dataframes


def convert_into(
        input_path, output_path, output_format="csv", java_options=None, **kwargs
):
    """Convert tables from PDF into a file.

    Args:
        input_path (file like obj):
            File like object of tareget PDF file.
        output_path (str):
            File path of output file.
        output_format (str, optional):
            Output format of this function (``csv``, ``json`` or ``tsv``).
            Default: ``csv``
        java_options (list, optional):
            Set java options

            Example:
                ``-Xmx256m``.
        kwargs (dict):
            Dictionary of option for tabula-java. Details are shown in
            :func:`build_options()`

    Returns:
        Nothing. Output file will be saved into `output_path`
    """

    if output_path is None or len(output_path) == 0:
        raise AttributeError("'output_path' shoud not be None or empty")

    kwargs["output_path"] = output_path
    kwargs["format"] = _extract_format_for_conversion(output_format)

    if java_options is None:
        java_options = []

    elif isinstance(java_options, str):
        java_options = shlex.split(java_options)

    # to prevent tabula_py from stealing focus on every call on mac
    if platform.system() == "Darwin":
        r = "java.awt.headless"
        if not any(filter(r.find, java_options)):
            java_options = java_options + ["-Djava.awt.headless=true"]

    path, temporary = localize_file(input_path)

    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    if os.path.getsize(path) == 0:
        raise ValueError(
            "{} is empty. Check the file, or download it manually.".format(path)
        )

    try:
        _run(java_options, kwargs, path)
    finally:
        if temporary:
            os.unlink(path)


def convert_into_by_batch(input_dir, output_format="csv", java_options=None, **kwargs):
    """Convert tables from PDFs in a directory.

    Args:
        input_dir (str):
            Directory path.
        output_format (str, optional):
            Output format of this function (csv, json or tsv)
        java_options (list, optional):
            Set java options like `-Xmx256m`.
        kwargs (dict):
            Dictionary of option for tabula-java. Details are shown in
            :func:`build_options()`

    Returns:
        Nothing. Outputs are saved into the same directory with `input_dir`
    """

    if input_dir is None or not os.path.isdir(input_dir):
        raise AttributeError("'input_dir' shoud be directory path")

    kwargs["format"] = _extract_format_for_conversion(output_format)

    if java_options is None:
        java_options = []

    elif isinstance(java_options, str):
        java_options = shlex.split(java_options)

    # to prevent tabula_py from stealing focus on every call on mac
    if platform.system() == "Darwin":
        r = "java.awt.headless"
        if not any(filter(r.find, java_options)):
            java_options = java_options + ["-Djava.awt.headless=true"]

    # Option for batch
    kwargs["batch"] = input_dir

    _run(java_options, kwargs)


def _extract_format_for_conversion(output_format="csv"):
    if output_format == "csv":
        return "CSV"

    if output_format == "json":
        return "JSON"

    if output_format == "tsv":
        return "TSV"

    if output_format == "dataframe":
        raise AttributeError("'output_format' has no attribute 'dataframe'")


def _extract_from(raw_json, pandas_options=None):
    """Extract tables from json.

    Args:
        raw_json (list):
            Decoded list from tabula-java JSON.
        pandas_options (dict optional):
            pandas options for `pd.DataFrame()`
    """

    data_frames = []
    if pandas_options is None:
        pandas_options = {}

    columns = pandas_options.pop("columns", None)
    columns, header_line_number = _convert_pandas_csv_options(pandas_options, columns)

    for table in raw_json:
        list_data = [
            [np.nan if not e["text"] else e["text"] for e in row]
            for row in table["data"]
        ]
        _columns = columns

        if isinstance(header_line_number, int) and not columns:
            _columns = list_data.pop(header_line_number)
            _columns = ["" if e is np.nan else e for e in _columns]

        data_frames.append(
            pd.DataFrame(data=list_data, columns=_columns, **pandas_options)
        )

    return data_frames


def _convert_pandas_csv_options(pandas_options, columns):
    """ Translate `pd.read_csv()` options into `pd.DataFrame()` especially for header.

    Args:
        pandas_options (dict):
            pandas options like {'header': None}.
        columns (list):
            list of column name.
    """

    _columns = pandas_options.pop("names", columns)
    header = pandas_options.pop("header", None)
    pandas_options.pop("encoding", None)

    if header == "infer":
        header_line_number = 0 if not bool(_columns) else None
    else:
        header_line_number = header

    return _columns, header_line_number


def build_options(kwargs=None):
    __options = []
    if kwargs is None:
        kwargs = {}
    options = kwargs.get("options", "")
    # handle options described in string for backward compatibility
    __options += shlex.split(options)

    DEPRECATED_OPTIONS = set(["spreadsheet", "nospreadsheet"])
    for option in set(kwargs.keys()) & DEPRECATED_OPTIONS:
        deprecated_option(option)

    # parse options
    pages = kwargs.get("pages", 1)
    if pages:
        __pages = pages
        if isinstance(pages, int):
            __pages = str(pages)
        elif type(pages) in [list, tuple]:
            __pages = ",".join(map(str, pages))

        __options += ["--pages", __pages]

    area = kwargs.get("area")
    relative_area = kwargs.get("relative_area")
    multiple_areas = False

    guess = kwargs.get("guess", True)

    if area:
        guess = False
        __area = area
        if type(area) in [list, tuple]:
            # Check if nested list or tuple for multiple areas
            if any(type(e) in [list, tuple] for e in area):
                for e in area:
                    __area = "{percent}{area_str}".format(
                        percent="%" if relative_area else "",
                        area_str=",".join(map(str, e)),
                    )
                    __options += ["--area", __area]
                    multiple_areas = True

            else:
                __area = "{percent}{area_str}".format(
                    percent="%" if relative_area else "",
                    area_str=",".join(map(str, area)),
                )
                __options += ["--area", __area]

    lattice = kwargs.get("lattice") or kwargs.get("spreadsheet")
    if lattice:
        __options.append("--lattice")

    stream = kwargs.get("stream") or kwargs.get("nospreadsheet")
    if stream:
        __options.append("--stream")

    if guess and not multiple_areas:
        __options.append("--guess")

    fmt = kwargs.get("format")
    if fmt:
        __options += ["--format", fmt]

    output_path = kwargs.get("output_path")
    if output_path:
        __options += ["--outfile", output_path]

    columns = kwargs.get("columns")
    if columns:
        __columns = ",".join(map(str, columns))
        __options += ["--columns", __columns]

    password = kwargs.get("password")
    if password:
        __options += ["--password", password]

    batch = kwargs.get("batch")
    if batch:
        __options += ["--batch", batch]

    silent = kwargs.get("silent")
    if silent:
        __options.append("--silent")

    return __options
