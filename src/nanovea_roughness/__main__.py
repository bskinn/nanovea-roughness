import os
from pathlib import Path
from time import strftime

import openpyxl as opxl
from tqdm import tqdm

from nanovea_roughness.core import (
    NanoveaData,
    nanovea_data_from_scanfile,
    Sa_calc as Sa,
    Sp_calc as Sp,
    Sq_calc as Sq,
    Sv_calc as Sv,
    Sz_calc as Sz,
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
            data = nanovea_data_from_scanfile(fpath)[NanoveaData.ZData]
            ws.append([fpath.name, Sa(data), Sz(data), Sq(data), Sp(data), Sv(data)])
        except Exception as e:
            ws.append([fpath.name, f"(processing failed: {e.__class__})"])

    wb.save(str(out_path))


if __name__ == "__main__":
    main()
