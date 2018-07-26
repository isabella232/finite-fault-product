# Web Product

## Introduction

Web product takes a directory of finite fault model files and creates a product for the U.S.G.S. 
[earthquake event pages](https://github.com/usgs/earthquake-eventpages). 

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
    <td colspan="3">* These files may be substituted with a properties.json file. See the example below.</td>
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
    <td>*Substitute property file</td>
    <td>properties.json</td>
    <td>properties.json</td>
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

## Property list created

### Standard properties

- area11: Area of the first segment.
- area_units: Units of the the area property. Always km*km.
- date: Date of the origin in the format `%Y-%m-%dT%H:%M:%S.%fZ`.
- depth: Depth of the origin.
- depth_units: Units of segment depth. Always km.
- dip11: Dip of the first segment.
- dip_units: Units of the dip property Always deg.
- eventsource: Event source network. Always us.
- eventsourcecode: Event id code. Example 1000dyad.
- latitude: Latitude of origin.
- length11: Length (along strike) or first segment.
- length_units: Units of the the length property. Always km.
- location: Description of location. Either a property provided the place property available at: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/[EVENTID].geojson' or '[LATITUDE], [LONGITUDE]'
- longitude: Longitude of origin.
- magnitude: Magnitude of origin.
- max_depth: Maximum depth of all segments.
- max_slip: Maximum slip of all segments.
- mechanism_dip: Overall dip of finite fault model.
- mechanism_rake: Overall rake of finite fault model.
- mechanism_strike: Overall strike of finite fault model.
- moment: Origin moment.
- moment_units: Units or moment property. Always dyne.cm.
- num_longwaves:  Number of long period surface waves selected.
- num_pwaves: Number of teleseismic broadband P waveforms.
- num_segments: Number of segments in the model.
- num_shwaves: Number of broadband SH waveforms.
- rake_units: Units of rake property. Always deg.
- rise_units: Units of rise property. Always s.
- slip_units: Units of slip property. Always m.
- strike11: Strike of the first segment.
- strike_units: Units of strike property. Always deg.
- trup_units: Units of trup property. Always s.
- width11: Width of first segment.
- width_units: Units of width property. Always km.
    
### Variable properties
Variables that may not be contained within other networks' fsp files.
- max_rake: Maximum rake of all segments.
- max_rise: Maximum rise of all segments.
- max_sf_moment: Maximum sf_moment of all segments.
- max_trup: Maximum trup of all segments.
For multisegment models, segment parameters will have different numbers. Two segment example:
- area12: Area of the first segment.
- area22: Area of the second segment.
- dip12: Dip of the first segment.
- dip22: Dip of the second segment.
- length12: Length (along strike) or first segment.
- length22: Length (along strike) or second segment.
- strike12: Strike of the first segment.
- strike22: Strike of the second segment.
- width12: Width of first segment.
- width22: Width of first segment.

For a single segment solution the mechanism properties and segment properties are synonymous.
For a two segment model, the segment properties are taken from each individual segment line, while the
mechanism is found in the mechanism line of the fsp file.
