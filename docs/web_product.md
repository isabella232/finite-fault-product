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
   - One product example: `sendproduct us us 1000dyad test/data/products/1000dyad -r`
   - Two product example: `sendproduct us us 10004u1y test/data/products/10004u1y_1 -ffm2 test/data/products/10004u1y_2 -r`
4. Delete the folders and send the product.
   - One product example: `sendproduct us 1000dyad test/data/products/1000dyad`
   - Two product example: `sendproduct us 10004u1y test/data/products/10004u1y_1 -ffm2 test/data/products/10004u1y_2`
5 (opt). Check that the product was send correctly.
   - One product example: `getproduct us 1000dyad ./output_events`
   - Two product example: `getproduct us 10004u1y ./output_events -t`
6 (opt). Delete an outdated product.
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

- area11: Calculated effective length of first subfault segment. See Comments.
- area_units: Units of the the area property. Always km*km.
- depth: Depth of the origin.
- depth_units: Units of segment depth. Always km.
- derived-magnitude: Magnitude calculated and available in the fsp file.
- derived-moment: Moment calculated and available in the fsp file.
- dip_units: Units of the dip property Always deg.
- eventsource: Event source network. Always us.
- eventsourcecode: Event id code. Example 1000dyad.
- eventtime: Date of the origin in the format %Y-%m-%dT%H:%M:%S.%fZ.
- latitude: Latitude of origin.
- length_units: Units of the the length property. Always km.
- length11: Calculated effective length of subfault segment. See Comments.
- location: Description of location. Either a property provided the place property available at: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/[EVENTID].geojson' or '[LATITUDE], [LONGITUDE]'
- longitude: Longitude of origin.
- max_slip: Maximum slip of all segments.
- mechanism_dip: Overall dip of finite fault model.
- mechanism_rake: Overall rake of finite fault model.
- mechanism_strike: Overall strike of finite fault model.
- model_area11: Area of the first segment.
- model_dip11: Dip of the first segment.
- model_length11: Length (along strike) or first segment.
- model_max_depth: Maximum depth of all segments.
- model_strike11: Strike of the first segment.
- model_width11: Width of first segment.
- moment_units: Units or moment property. Always dyne.cm.
- num_longwaves: Number of long period surface waves selected.
- num_pwaves: Number of teleseismic broadband P waveforms.
- num_segments: Number of segments in the model.
- num_shwaves: Number of broadband SH waveforms.
- rake_units: Units of rake property. Always deg.
- rise_units: Units of rise property. Always s.
- slip_units: Units of slip property. Always m.
- strike_units: Units of strike property. Always deg.
- width_units: Units of width property. Always km.
- width11: Calculated effective width of first subfault segment. See Comments.
- Variable Properties
- Variables that may not be contained within other networks' fsp files.

- max_rise: Maximum rise of all segments. For multisegment models, segment parameters will have different numbers. Two segment example:
- area12: Calculated effective area of the first subfault segment. See Comments.
- area22: Calculated effective area of the second subfault segment. See Comments.
- model_area12: Area of the first segment.
- model_area22: Area of the second segment.
- model_dip12: Dip of the first segment.
- model_dip22: Dip of the second segment.
- model_length12: Length (along strike) or first segment.
- model_length22: Length (along strike) or second segment.
- length12: Calculated effective length (along strike) of first subfault segment. See Comments.
- length22: Calculated effective length (along strike) of second subfault segment. See Comments.
- model_strike12: Strike of the first segment.
- model_strike22: Strike of the second segment.
- model_width12: Width of first segment.
- model_width22: Width of first segment.
- width12: Calculated effective width of first subfault segment. See Comments
- width22: Calculated effective width of second subfault segment. See Comments.

### Comments
**Calculated and Model Properties**
Properties prefixed with model_ are set model parameters. For example, model_width11 is the set width of segment 1 of the model space, while width11 is the calculated width of the rupture.

[Calculations of effective length, width](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/fault/fault.py#L337), and area properties were derived from the autocorrelation width given by [Mai et al](https://www.researchgate.net/publication/228607551_Source_scaling_properties_from_finite-fault-rupture_models):

<a href="https://www.codecogs.com/eqnedit.php?latex=W^{ACF}_{equivalent}&space;=&space;\frac{\int^{\infty}_{-\infty}(f*f)dx}{f&space;*&space;f|_{x=0}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?W^{ACF}_{equivalent}&space;=&space;\frac{\int^{\infty}_{-\infty}(f*f)dx}{f&space;*&space;f|_{x=0}}" title="W^{ACF}_{equivalent} = \frac{\int^{\infty}_{-\infty}(f*f)dx}{f * f|_{x=0}}" /></a>

Note: For the effective length/width the slip is [thresholded](https://github.com/hschovanec-usgs/finite-fault-product/blob/master/fault/fault.py#L531).

**Mechanism and Segment Properties**
For a single segment solution the mechanism properties and model_segment properties are synonymous. For a two segment model, the model_segment properties are taken from each individual segment line, while the mechanism is found in the mechanism line of the fsp file.
