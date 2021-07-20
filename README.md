Nanovea ST-400 Surface Roughness Calculator
===================

The [Nanovea ST-400](https://nanovea.com/instruments/st400/) is a non-contact optical profilometer that
measures the topography of workpiece surfaces as a two-dimensional array of heights.
While the software shipped with the instrument for analysis of the resulting
profile data is highly capable in many regards, its algorithms for calculating
two-dimensional roughness metrics have been found to be incorrect.

The purpose of this repository and `nanovea_roughness` Python package is
to provide a tool to easily and correctly carry out calculation of these
2-D roughness metrics, starting from scan data exported as text. The exported
data is generated in a standard fashion, which is accounted for by the
`nanovea_data_from_scanpath` method.

Alternatively, if surface data is available from another source, that data
can be used by converting it into a `numpy.ndarray` by whatever suitable means.

This analysis is meant for scans covering relatively small areas of a workpiece
(~50-100 um along each side of the scan area) at a relatively high point density
(scan steps of 0.5-2.0 um), where topography at macroscopic and waviness length scales
can safely be neglected and a planar reference surface is appropriate for the
roughness calculation. Note that in order for determination of the planar
reference surface to work correctly, the *x* and *y* steps
***must be uniform*** across the full scan area, though it is fine if
the *x* and *y* steps differ from each other.

Installation
-------

pip-install this repository into a suitable virtual environment:

```
(env) $ pip install git+https://github.com/bskinn/nanovea-roughness
```

Usage
-----

Import the `nanovea_roughness` package:

```
>>> import nanovea_roughness as nr
```

Import the data from a scan datafile (the required data format can be seen [here](https://github.com/bskinn/nanovea-roughness/blob/master/test_data/test1.txt)):

```
>>> data = nr.nanovea_data_from_scanpath("test.txt")
>>> data
{<NanoveaData.Filename: 'fname'>: 'test.txt', <NanoveaData.Counts: 'counts'>: [101, 101], <NanoveaData.Incs: 'incs'>: [0.005, 0.005], <NanoveaData.ZData: 'zdata'>: array([[218.4546, 219.1168, 222.2589, ..., 270.6953, 271.7816, 272.0135],
       [207.6688, 207.887 , 211.8543, ..., 261.9275, 263.4182, 264.2017],
       [208.7452, 208.8223, 216.0127, ..., 264.4853, 266.1218, 266.8536],
       ...,
       [231.2596, 231.1892, 232.7189, ..., 278.799 , 277.9822, 276.8931],
       [231.4105, 231.8307, 231.9724, ..., 278.7672, 277.8636, 277.7744],
       [231.4407, 231.9086, 233.7686, ..., 277.9236, 277.1981, 277.3815]])}
```

The path to the data file can be provided either as a string, or as a
[`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path).

All that's needed for the roughness calculations is the z-data array
(though the `data` dict also provides information on the 
x/y grid dimensions and point spacings, as shown above):

```
>>> arr = data[nr.NanoveaData.ZData]
>>> arr
array([[218.4546, 219.1168, 222.2589, ..., 270.6953, 271.7816, 272.0135],
       [207.6688, 207.887 , 211.8543, ..., 261.9275, 263.4182, 264.2017],
       [208.7452, 208.8223, 216.0127, ..., 264.4853, 266.1218, 266.8536],
       ...,
       [231.2596, 231.1892, 232.7189, ..., 278.799 , 277.9822, 276.8931],
       [231.4105, 231.8307, 231.9724, ..., 278.7672, 277.8636, 277.7744],
       [231.4407, 231.9086, 233.7686, ..., 277.9236, 277.1981, 277.3815]])
```

A helper function is provided to retrieve just the z-data array:

```
>>> nr.zdata_from_scanpath("test.txt")
array([[218.4546, 219.1168, 222.2589, ..., 270.6953, 271.7816, 272.0135],
       [207.6688, 207.887 , 211.8543, ..., 261.9275, 263.4182, 264.2017],
       [208.7452, 208.8223, 216.0127, ..., 264.4853, 266.1218, 266.8536],
       ...,
       [231.2596, 231.1892, 232.7189, ..., 278.799 , 277.9822, 276.8931],
       [231.4105, 231.8307, 231.9724, ..., 278.7672, 277.8636, 277.7744],
       [231.4407, 231.9086, 233.7686, ..., 277.9236, 277.1981, 277.3815]])
```

`arr` can then be fed into the appropriate `S{}` function in order
to obtain the roughness metric of interest:

```
>>> nr.Sa(arr)
9.340576069231256
```

Administrative
-------

Source on [GitHub](https://github.com/bskinn/nanovea-roughness).  Bug reports
and feature requests are welcomed at the
[Issues](https://github.com/bskinn/nanovea-roughness/issues) page there.

Copyright (c) Brian Skinn 2020

License: The MIT License. See [LICENSE.txt](https://github.com/bskinn/nanovea-roughness/blob/master/LICENSE.txt)
for full license terms.
