import os
from pathlib import Path

import openpyxl as opxl
from tqdm import tqdm

# from neutrino_polzn.core import NeutrinoPolzn


def main():
    base_path = Path(os.getcwd())

    for fpath in tqdm([p for p in base_path.iterdir() if p.suffix == ".txt"]):
        print(str(fpath))


if __name__ == "__main__":
    main()