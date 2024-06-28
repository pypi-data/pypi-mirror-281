"""
This package is used to interprets and interprets lab mice behaviour using computer vision.
The package allows users to perform the entire analytics pipeline from raw lab footage to
interpretable plotted and tabulated data for different analysises. This pipeline includes:

- Formatting raw videos to a desired mp4 format (e.g. user defined fps and resolution)
- Performing stance detection on the mp4 file to generate an annotated mp4 file and file that tabulates the x-y coordinates of the subject's body points in each video frame. DeepLabCut is used to perform this.
- Preprocessing the coordinates file
- Extracting meaningful data analysis from the preprocessed coordinates file
"""

import logging
import logging.config
import os
import warnings

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from behavysis_core.constants import PLOT_DPI, PLOT_STYLE, Folders
from behavysis_core.mixins.io_mixin import IOMixin

#####################################################################
#               FILTERING STDOUT WARNINGS
#####################################################################

warnings.filterwarnings("ignore")

#####################################################################
#           INITIALISE MPL PLOTTING PARAMETERS
#####################################################################


# Makes graphs non-interactive (saves memory)
matplotlib.use("Agg")  # QtAgg

sns.set_theme(style=PLOT_STYLE)

plt.rcParams["figure.dpi"] = PLOT_DPI
plt.rcParams["savefig.dpi"] = PLOT_DPI

#####################################################################
#           SETTING UP LOGGING
#####################################################################

logging.basicConfig(level=logging.INFO)


#####################################################################
#               MAKING SCRIPTS
#####################################################################


def make_project(root_dir: str, overwrite: bool = False) -> None:
    """
    Makes a script to run a behavysis analysis project.

    Copies the `run.py` script and `default_configs.json` to `root_dir`.
    """
    # Making the root folder
    os.makedirs(root_dir, exist_ok=True)
    # Making each subfolder
    for f in Folders:
        os.makedirs(os.path.join(root_dir, f.value), exist_ok=True)
    # Copying the default_configs.json and run.py files to the project folder
    for i in ["default_configs.json", "run.py"]:
        # Getting the file path
        dst_fp = os.path.join(root_dir, i)
        # If not overwrite and file exists, then don't overwrite
        if not overwrite and os.path.exists(dst_fp):
            continue
        # Saving the template to the file
        IOMixin.save_template(
            i,
            "behavysis_pipeline",
            "script_templates",
            dst_fp,
        )


def make_behav_classifier(root_dir: str, overwrite: bool = False) -> None:
    """
    Makes a script to build a BehavClassifier.

    Copies the `train_behav_classifier.py` script to `root_dir/behav_models`.
    """
    models_dir = os.path.join(root_dir, "behav_models")
    # Making the project root folder
    os.makedirs(models_dir, exist_ok=True)
    # Copying the default_configs.json and run.py files to the project folder
    for i in ["train_behav_classifier.py"]:
        # Getting the file path
        dst_fp = os.path.join(models_dir, i)
        # If not overwrite and file exists, then don't overwrite
        if not overwrite and os.path.exists(dst_fp):
            continue
        # Saving the template to the file
        IOMixin.save_template(
            i,
            "behavysis_pipeline",
            "script_templates",
            dst_fp,
        )
