Status
=======

[![Build Status](https://travis-ci.org/hschovanec-usgs/finite-fault-product.svg?branch=master)](https://travis-ci.org/hschovanec-usgs/finite-fault-product)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/81d612b63c864f3fb894f4e5bec90b49)](https://www.codacy.com/app/hschovanec-usgs/finite-fault-product?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hschovanec-usgs/finite-fault-product&amp;utm_campaign=Badge_Grade)

[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/81d612b63c864f3fb894f4e5bec90b49)](https://www.codacy.com/app/hschovanec-usgs/finite-fault-product?utm_source=github.com&utm_medium=referral&utm_content=hschovanec-usgs/finite-fault-product&utm_campaign=Badge_Coverage)

[![Waffle.io - Columns and their card count](https://badge.waffle.io/hschovanec-usgs/finite-fault-product.svg?columns=all)](https://waffle.io/hschovanec-usgs/finite-fault-product)


# finite-fault-product

Load finite fault data and create products.

## fault
Designed to analyze finite fault models and time series.
* `fault.py` Class to analyze fault models.

### fault.io
fault.io is designed to read finite fault data from fsp, dat, and syn files.

 * `fsp.py` Load rupture model.
 * `timeseries.py` Load data and synthetic seismograms.

## product
product is designed to create eventpages and ShakeMap products.
* `web_product.py` Create web product from time series and fault data. (Under construction)
* `pdl.py` Contains methods for sending products to pdl.
* `shakemap_product.py` Create shakemap product from time series and fault data. (Unavailable)


# Property list created by `web_product.py`
## Standard properties

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
    
## Variable properties
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

For a single segment solution the mechanism properties and segment properties are synonymous. For a two segment model, the segment properties are taken from each individual segment line, while the mechanism is found in the mechanism line of the fsp file.
