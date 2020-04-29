# ICM 2020 Problem F Model

Model of land change of islands. Converts grey-scale heghtmap image to CSV,
then calculates yearly precent change of land. This model is described in more
detail in the [paper](doc/protect-and-preserve.pdf) that it was made for.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes.

### Prerequisites

ICM 2020 Problem F Model is written in python, and requires the following
modules to be installed.

* [NumPy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [plotly](https://plotly.com/)
* [Pillow](https://python-pillow.org/)

Install them with using pip.

```
pip install numpy
pip install pandas
pip install plotly
pip install Pillow
```

### Installing

This project is currently for development and testing only. Clone the
repository to your local machine.

```
git clone https://github.com/RileyKrall/ICM-2020-Problem-F-Model.git
```

Run the script from the directory after cloning.

```
cd ICM-2020-Problem-F-Model.git
python MCM2020LandMassModel.py
```

## Built With

* [terrain.party](http://terrain.party/) - Height map data

## Authors

* **Riley Krall** - *Model* - <https://github.com/RileyKrall>

See also the list of
[contributors](https://github.com/RileyKrall/ICM-2020-Problem-F-Model/contributors)
who participated in this project.

## License

This project is licensed under the MIT License, see [LICENSE.txt](LICENSE.txt)
for details.
