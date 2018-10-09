# Web Product

- [Introduction](#introduction)
- [Instructions](#instructions)
- [Requirements](#requirements)
  * [Required Files](#required-files)
  * [Optional Files](#optional-files)
- [Property List Created](#property-list-created)
  * [Standard Properties](#standard-properties)
  * [Variable Properties](#variable-properties)


## Introduction

Web product takes a directory of finite fault model files and creates a product for the U.S.G.S.
[earthquake event pages](https://github.com/usgs/earthquake-eventpages). See the provided [notebooks](https://github.com/hschovanec-usgs/finite-fault-product/tree/master/notebooks) for examples of API use.

## Instructions

1. [Install](https://github.com/hschovanec-usgs/finite-fault-product#installing) the finite-fault-product packages.
2. Create a directory containing all finite fault model files.
    - Note: If the model includes two equally valid solutions, create two directories.
3. Review the product created. Product files will be written to ~/pdlout/[EVENTCODE]
   - One product example: `sendproduct us us 1000dyad tests/data/products/1000dyad -r`
   - Two product example: `sendproduct us us 10004u1y tests/data/products/10004u1y_1 -ffm2 tests/data/products/10004u1y_2 -r`
4. Delete the folders and send the product.
   - One product example: `sendproduct us us 1000dyad tests/data/products/1000dyad`
   - Two product example: `sendproduct us us 10004u1y tests/data/products/10004u1y_1 -ffm2 tests/data/products/10004u1y_2`
5. (opt). Check that the product was sent correctly.
   - One product example: `getproduct us us 1000dyad ./output_events`
   - Two product example: `getproduct us us 10004u1y ./output_events -t`
6. (opt). Delete an outdated product.
   - One product example: `deleteproduct us us 1000dyad`
    - Two product example (Delete the seconds model): `getproduct us us 10004u1y -t -m 2`

## Requirements
In order to create the web product a folder containing the folowing files is required. Note: Duplicates of files will not be sent.

### Required Files
Failure to include these files will result in an error
<table>
  <tr>
    <th>File Description</th>
    <th>File Pattern Searched</th>
    <th>Example Input Name</th>
  </tr>
  <tr>
    <td>Moment rate image</td>
    <td>*mr*.png</td>
    <td>mr.png</td>
  </tr>
  <tr>
    <td>Base map image</td>
    <td>*base*.png</td>
    <td>1000dyad_basemap.png</td>
  </tr>
  <tr>
    <td>Slip image</td>
    <td>*slip*.png</td>
    <td>1000dyad_slip2.png</td>
  </tr>
  <tr>
    <td>Analysis description file</td>
    <td>analysis.txt</td>
    <td>analysis.txt</td>
  </tr>
  <tr>
    <td>Finite-source parameter (complete inversion) file</td>
    <td>*.fsp</td>
    <td>1000dyad.fsp</td>
  </tr>
  <tr>
    <td>*Long waveform file</td>
    <td>synm.str_low</td>
    <td>synm.str_low</td>
  </tr>
  <tr>
    <td>*Waveform file</td>
    <td>Readlp.das</td>
    <td>Readlp.das</td>
  </tr>
  <tr>
    <td colspan="3">* These files may be substituted with a wave_properties.json file. See the example below.</td>
  </tr>
</table>

### Optional Files
These files are note required, but are recommended and will be looked for.
<table>
  <tr>
    <th>File Description</th>
    <th>File Pattern Searched</th>
    <th>Example Input Name</th>
  </tr>
  <tr>
    <td>Compressed folder of waveform plots</td>
    <td>waveplots.zip</td>
    <td>waveplots.zip</td>
  </tr>
  <tr>
    <td>CMT solution file</td>
    <td>*CMTSOLUTION*</td>
    <td>CMTSOLUTION</td>
  </tr>
  <tr>
    <td>Coulomb input file</td>
    <td>*coulomb.inp</td>
    <td>1000dyad_coulomb.inp</td>
  </tr>
  <tr>
    <td>Basic inversion file</td>
    <td>*.param</td>
    <td>1000dyad.param</td>
  </tr>
  <tr>
    <td>Model KML file</td>
    <td>*kml</td>
    <td>1000dyad.kml</td>
  </tr>
  <tr>
    <td>Model KMZ file</td>
    <td>*kmz</td>
    <td>1000dyad.kmz</td>
  </tr>
  <tr>
    <td>Surface deformation file</td>
    <td>*disp</td>
    <td>1000dyad.disp</td>
  </tr>
  <tr>
    <td>Moment rate ASCII file</td>
    <td>*.mr</td>
    <td>1000dyad.mr</td>
  </tr>
  <tr>
    <td>*Substitute wave property file</td>
    <td>wave_properties.json</td>
    <td>wave_properties.json</td>
  </tr>
  <tr>
    <td colspan="3">* This file may be used as a substitute for the </td>
  </tr>
</table>

Note: If waveplots.zip is not included but plot images are (files with the pattern "*wave_*.png"), a zip file will be created for these images.


## File name changes
File names are standardized for each event.
<table>
  <tr>
    <th>Product File Description</th>
    <th>Standard File Name</th>
  </tr>
  <tr>
    <td>Moment rate image</td>
    <td>moment_rate.png</td>
  </tr>
  <tr>
    <td>Base map image</td>
    <td>basemap.png</td>
  </tr>
  <tr>
    <td>Slip image</td>
    <td>slip.png</td>
  </tr>
  <tr>
    <td>Analysis description file</td>
    <td>analysis.html</td>
  </tr>
  <tr>
    <td>Finite-source parameter (complete inversion) file</td>
    <td>complete_inversion.fsp</td>
  </tr>
  <tr>
    <td>Finite fault model GeoJSON</td>
    <td>FFM.geojson</td>
  </tr>
  <tr>
    <td>Download contents file</td>
    <td>contents.xml</td>
  </tr>
  <tr>
    <td>Product properties file</td>
    <td>properties.json</td>
  </tr>
  <tr>
    <td>Page html file</td>
    <td>finite_fault.html</td>
  </tr>
  <tr>
    <td>*Compressed folder of waveform plots</td>
    <td>waveplots.zip</td>
  </tr>
  <tr>
    <td>*CMT solution file</td>
    <td>CMTSOLUTION</td>
  </tr>
  <tr>
    <td>*Coulomb input file</td>
    <td>coulomb.inp</td>
  </tr>
  <tr>
    <td>*Basic inversion file</td>
    <td>basic_inversion.param</td>
  </tr>
  <tr>
    <td>*Model kml file</td>
    <td>finite_fault.kml</td>
  </tr>
  <tr>
    <td>*Model kml file</td>
    <td>finite_fault.kmz</td>
  </tr>
  <tr>
    <td>*Surface deformation file</td>
    <td>surface_deformation.disp</td>
  </tr>
  <tr>
    <td>*Moment rate ASCII file</td>
    <td>moment_rate.mr</td>
  </tr>
  <tr>
    <td colspan="2">*Indicates files that will not be included if not provided by the user.</td>
  </tr>
</table>

## Property List Created

### Standard Properties

- average-rise-time: [Average rise in seconds](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L9).
- average-rupture-velocity: [Average ruptrue velocity in kilometers per second](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L9).
- depth: Depth of the rupture plane in kilometers.
- derived-magnitude: Magnitude calculated and available in the [fsp file](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L7).
- derived-magnitude-type: Magnitude type. Always [Mw](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L7).
- eventsource: Event source network. Always us.
- eventsourcecode: Event id code. Example 1000dyad.
- eventtime: Date of the origin in the format %Y-%m-%dT%H:%M:%S.%fZ.
- hypocenter-x: rupture nucleation point in the fault plane (starting at top-left corner)
- hypocenter-z: rupture nucleation point in the fault plane (starting at top-left corner)
- latitude: Latitude of origin.
- location: Description of location. Either a property provided the place property available at: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/[EVENTID].geojson' or '[LATITUDE], [LONGITUDE]'
- longitude: Longitude of origin.
- maximum-frequency: [Maximum frequency of bandpass filtered seismic data](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L13).
- maximum-slip: Maximum slip of all segments. Inits are m.
- minimum-frequency: [Minimum frequency of bandpass filtered seismic data](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L13).
- model-dip: [Dip of the fault plane in degrees](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L8).
- model-length: [Length of the rupture plane in kilometers](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L7).
- model-rake: [Rake of the model in degrees](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L8).
- model-strike: [Strike of the fault plane in degrees](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L8).
- model-top: [Vertical depth to the top of the rupture plane](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L8).
- model-width: [Width of the rupture plane in kilometers](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L7).
- number-longwaves: Number of long period surface waves selected.
- number-pwaves: Number of teleseismic broadband P waveforms.
- number-shwaves: Number of broadband SH waveform
- scalar-moment: Moment calculated and available in the [fsp file](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000482z_us_3_p000482z.fsp#L7) in Newton * meter.
- segments: Number of segments in the model. [There may be two or more segments](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000714t_us_4_p000714t.fsp#L15).
- segment-1-dip: Model dip of the first segment. Units are degrees.
- segment-1-strike: [Model strike of the first segment](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000714t_us_4_p000714t.fsp#L52). Units are degrees.
- subfault-1-area: Calculated effective area of first subfault. See Comments. Units are km*km.
- subfault-1-length: Calculated effective length of subfault. See Comments. Units are km*km.
- subfault-1-width: Calculated effective width of first subfault. See Comments.
- time-windows: [Number of time windows used in the inversion](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000714t_us_4_p000714t.fsp#L15).
- velocity-function: [Type](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000714t_us_4_p000714t.fsp#L17) of velocity funtion used in the inversion.


### Variable Properties
Variables that may not be contained within other networks' fsp files.

- maximum-rise: Maximum rise of all segments. Units are seconds.

For multisegment models, segment parameters will have different numbers. Two segment example:

- segment-2-dip: [Dip of the second segment](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/fsp/usp000714t_us_4_p000714t.fsp#L168).
- segment-2-strike: Strike of the second segment.
- subfault-2-area: Calculated effective area of the second subfault. See Comments.
- subfault-2-length: Calculated effective length (along strike) of second subfault. See Comments.
- subfault-2-width: Calculated effective width of second subfault. See Comments.

### Comments
**Calculated and Model Properties**
Properties prefixed with model- are set model parameters. For example, model-strike is the strike used to [create the model](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/products/000714t/p000714t.fsp#L8), while segment-1-strike is the strike of the individual [segment](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/tests/data/products/000714t/p000714t.fsp#L52).

[Calculations of effective length, width](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/fault/fault.py#L337), and area properties were derived from the autocorrelation width given by [Mai et al](https://www.researchgate.net/publication/228607551_Source_scaling_properties_from_finite-fault-rupture_models):

<a href="https://www.codecogs.com/eqnedit.php?latex=W^{ACF}_{equivalent}&space;=&space;\frac{\int^{\infty}_{-\infty}(f*f)dx}{f&space;*&space;f|_{x=0}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?W^{ACF}_{equivalent}&space;=&space;\frac{\int^{\infty}_{-\infty}(f*f)dx}{f&space;*&space;f|_{x=0}}" title="W^{ACF}_{equivalent} = \frac{\int^{\infty}_{-\infty}(f*f)dx}{f * f|_{x=0}}" /></a>

Note: For the effective length/width the slip is [thresholded](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/fault/fault.py#L531).

**Model and Segment Properties**
For a single segment solution the model properties and segment-1 properties are synonymous. For a two segment model, the model properties are taken from each individual segment line, while the model is found in the mechanism line of the fsp file.
