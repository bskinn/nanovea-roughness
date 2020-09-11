r"""*Main execution module for* ``nanovea_roughness``.

``nanovea_roughness`` is a tool for automatically carrying out
surface roughness calculations on Nanovea ST-400 profilometry scan
data exports.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    11 Sep 2020

**Copyright**
    \(c) Brian Skinn 2020

**Source Repository**
    http://www.github.com/bskinn/nanovea-roughness

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import os
from pathlib import Path
from time import strftime

import openpyxl as opxl
from tqdm import tqdm

from nanovea_roughness import (
    NanoveaData,
    nanovea_data_from_scanpath,
    Sa,
    Sp,
    Sq,
    Sv,
    Sz,
)


def main():
    base_path = Path(os.getcwd())

    out_path = base_path / f"roughness_{strftime('%Y%m%d_%H%M%S')}.xlsx"

    wb = opxl.Workbook()
    ws = wb.active
    ws.title = "Roughness Data"

    ws.append(["", "(Units typically um)"])
    ws.append(["Data File", "Sa", "Sz", "Sq", "Sp", "Sv"])

    for fpath in tqdm([p for p in base_path.iterdir() if p.suffix == ".txt"]):
        try:
            data = nanovea_data_from_scanpath(fpath)[NanoveaData.ZData]
            ws.append([fpath.name, Sa(data), Sz(data), Sq(data), Sp(data), Sv(data)])
        except Exception as e:
            ws.append([fpath.name, f"(processing failed: {e.__class__})"])

    wb.save(str(out_path))


if __name__ == "__main__":
    main()
