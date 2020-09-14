r"""*Package definition for* ``nanovea_roughness``.

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
    *(pending)*

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from nanovea_roughness.core import (
    NanoveaData,
    nanovea_data_from_scanpath,
    Sa_calc as Sa,
    Sp_calc as Sp,
    Sq_calc as Sq,
    Sv_calc as Sv,
    Sz_calc as Sz,
)
