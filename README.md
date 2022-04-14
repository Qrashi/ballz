![DeepSource issues](https://deepsource.io/gh/Qrashi/ballz.svg/?label=active+issues&show_trend=true&token=Dow_XNocdGMrkQMloU73omFl)
![GitHub issues](https://img.shields.io/github/issues-raw/Qrashi/ballz)

# ballz

Ballz is a simulation of two balls on an elastic band. It should visualize problem 11 of
the [2022 IYPT problems](https://www.iypt.org/wp-content/uploads/2021/07/problems2022_signed.pdf).

## Installation

1. If not already installed, install git.
    1. If you are on windows, [download here](https://git-scm.com/download/win)
    2. On linux, just use your standard package manager
2. Clone this repository ``git clone https://github.com/Qrashi/ballz.git``
3. cd into the `ballz` directory
4. Run ``python ballz.py``

#### Please note that windows is not offically supported, you will likely encounter bugs

The ballz.py file will automatically update the project and install dependencies for you.

#### In case something breaks

Try running ``git fetch origin`` and ``git pull origin`` to update to the newest version

#### config.json

Allows you to customize various aspects about the simulation

* enable_git_auto_update: (true | false) Wether to enable auto downloading new updates
* font: ("font name") Font to use
* max_performance: (true | false) Enable / disable max_performance mode
* disable_log: (true | false) disable or enable data logging

#### Changing the setup

If you would like to run the simulation with different constants or different input parameters, change the contents of
the ``scenarios.json`` file. <br>
In order to add a new scenario to which you can switch using the arrow keys, please add another "block of data" like
that:

```json
{
  "scenarios": [
    {
      #
    The
    predefined
    scenario
    },
    #
    Add
    a,
    and
    put
    your
    new
    scenario
    in
    the
    lines
    below
    {
      #
    Put
    the
    values
    for
    your
    simulation
    here
    (look
    at
    the
    default
    to
    see
    which
    values
    you
    have
    to
    provide.)
    }
  ]
}
```
