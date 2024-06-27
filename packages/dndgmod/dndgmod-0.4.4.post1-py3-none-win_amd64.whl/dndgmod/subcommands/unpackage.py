from typing import Annotated
from tkinter import Tk, filedialog
from zipfile import ZipFile

import typer
import os
import subprocess
from pathlib import Path
from shutil import rmtree


def unpackage(
        ctx: typer.Context,
):
    logger = ctx.obj["logger"]

    Tk().withdraw()
    logger.info("Opening a file dialog, select where your packaged mod is.")
    dndg_file_path = Path(filedialog.askopenfilename(title="Open Packaged DnDGMod Mod...",
                                                     filetypes=[("Packaged DnDGMod Mod", ".zip")],
                                                     defaultextension=".zip"))
    mod_directory: Path = ctx.obj["data_directory"] / "mods" / dndg_file_path.name.rstrip(".zip")
    with ZipFile(dndg_file_path, "r") as archive:
        archive.extractall(mod_directory)
    if not (mod_directory / "mod.yaml").exists():
        rmtree(mod_directory)
        raise ValueError("The .zip file was not in dndgmod format")
    logger.info(f"Unpackaging of {dndg_file_path.name} successful!")
