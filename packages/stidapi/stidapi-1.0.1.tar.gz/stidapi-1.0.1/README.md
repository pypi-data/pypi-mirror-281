# STIDapi-python

A simple wrapper package to interface Equinor [STIDapi](https://stidapi.equinor.com/).  
Used to get plant, systen and tag and (future) doc data from STID rest api.


## Use

Try it out by running the [demo](examples/demo.py).

## Installing

To **install** call the following from your project environment:  
`pip install git+https://github.com/equinor/STIDapi-python.git`

To **upgrade** call the following from your project environment:  
`pip install --upgrade git+https://github.com/equinor/STIDapi-python.git`

To include in your project, add the following to your requirements file:  
`git+https://github.com/equinor/STIDapi-python.git`

or in requirements setup.py:  
`'stidapi @ git+https://github.com/equinor/STIDapi-python'` 

or in pyproject.toml:  
`stidapi = { git = "https://github.com/Equinor/stidapi-python" }` 


## Developing / testing

Poetry is preferred for developers. Install with required packages for testing and coverage:  
`poetry install`

Call `poetry run pytest` to run tests.

To generate coverage report in html run `poetry run pytest --cov=stidapi tests/ --cov-report html`

