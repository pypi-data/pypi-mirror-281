# `lseg_analytics` python library

Python Client Library for "LSEG Analytics as a Service" API's.

Otherwise, called "SDK". But it's not, really. Just an API client library. At least at the moment. 

[//]: # (This version of a library works only with the [mock-server]&#40;https://gitlab.dx1.lseg.com/206243/dapi/python-libraries/aaas/aaas-mock-server&#41;,)
[//]: # (because we don't have other implementations of the new API.)

Currently, library works without configuration.

## Getting Started

## Usage examples

Completely useless example, but at least it demonstrates location of the calendar module and class and a couple of basic concepts:

```python
from lseg_analytics.reference_data.calendars import Calendar
calendar = Calendar()
calendar.description.name = "New Calendar"
calendar.save()
```

## Modules Structure

- `common` - contains models that can be used in different API modules
- `logging` - logging configuration
- `exceptions`
- API modules
  - `reference_data`
    - `calendars`
    - `currencies`
    - `cross_currencies`
  - `market_data`
    - `fx_forward_curves`
  - `instruments`
    - `fx_spots`
    - `fx_forwards`

## API module structure

- each API Module has a main object, which has the same name as a module, but in singular form
  - Examples
    - `reference_data.calendars`: `Calendar`
    - `reference_data.currencies`: `Currency`
    - `reference_data.cross_currencies`: `CrossCurrency`
    - `market_data.fx_forward_curves`: `FxForwardCurve`
    - `instruments.fx_spots`: `FxSpot`
    - `instruments.fx_forwards`: `FxForward`
  - Instance of this object represents corresponding resource on the server
- each API Module has functions `load`, `search`, `delete`
- **TODO**: Resource methods

## Documentation

The latest version of the library documentation available [here.](https://206243.pages.dx1.lseg.com/dapi/python-libraries/aaas-sdk-python/index.html)