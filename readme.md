# Fiber alignment automation library

This library controls the Thorlabs BPC203 piezoelectric controller that actuates the DRV517 Piezoelectric Actuator

## Usage

This module can be used by simply including the files `bcolours.py` and `bpc203.py` in your project directory. 

Alternatively, if you are a strict adherent to Git best practices, you can add this repository as a submodule for your git repo using 

```
$ git submodule add https://github.com/lixiii/BPC203.git
```

**Alternatively, a setup script has been provided and the package can be installed to the home directory by the following command**
```
$ sudo python3 setup.py install
```

## Unit test

All unit tests are written using pytest module and can be run by 

```
$ sudo pytest test.py
```

## Thorlabs documentation

The documentation for the communication protocol can be found at https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf