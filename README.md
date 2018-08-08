# RSSI Python module
With IoT projects at an all time high, there is a continuous need for positioning and localization systems in places where 
GPS localiztion is not available. RSSI-based localization offers the ability to find an unknown position using the 
RSSI (relative received signal strength) of nearby access-points (wifi routers). RSSI-based localiztion algortihms require 'n' number
of access points, where 'n' >= 3 access points. With the development of wireless are networks and smart devices, the number
of WIFI access point in buildings is increasing, as long as a mobile smart device can detect three or more
known WIFI hotspots’ positions, it would be relatively easy to realize self-localization (Usually WIFI access points
locations are fixed, but modifications acn be made for moving access points).

This module contains two classes, 'RSSI_Scan' and 'RSSI_Localizer'.
RSSI_Scan is used to find and return information on all available access points, within range.
A 'networks' list can be provided as an argument to filter networks of interest.

RSSI_Localizer is used for self-localization, using the information returned by RSSI_Scan. this 
class can not be used, without the use of three or more known accesspoints.

The algorithm used in this module is entirely base off of Xiuyan Zhu's, Yuan Feng's 
'RSSI-based Algorithm for Indoor Localization' paper, published here: https://file.scirp.org/pdf/CN_2013071010352139.pdf

There are exisitng Python and Java modules for network scanning and RSSI-localization, but there was a need for 
a more extensive package that scales for a virtually unlimited number of Wifi access points. An emphasis was placed on documentation
and easability of use. Both classes cna be used independently, if desired.

This package asdesigned to be as light and effciient as possible, for use in real-time or soft real-time environments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

A Python interpreter will be neccesary to run this module. Package is compatible with Python 2.x or 3.x.

The NumPy library will need to be installed, before using this package. We will be updating this package to include the NumPy dependency. See 'Built With' section for installation of NumPy.

### Installing

The RSSI package can be installed via PIP or by cloning this GitHub repo. Future releases will include a package installer for Linux.

Say what the step will be

```
pip install rssi
```

OR

```
git clone XXXX
```
### Classes

The RSSI package comes woth two classes to help you with scanning for access points (RSS_Scan) and RSSi-based, self-localization (RSSI_Localizer).
Methods for both classes can be found below.

### RSSI_Scan methods

#### getRawNetworkScan()
```
# Description:
    # Runs the Ubuntu command 'iwlist' to scan for available networks.
    # Returns the raw console window output (unparsed).
# ----------------------------------------------------------------
# Input: (optional) 
    #   sudo: bool; defaults to false. False will not refresh the 
    #         network interface upon query. Sudo=true will require 
    #         the user will need to enter a sudo password at runtime.
# ----------------------------------------------------------------
# Returns: Raw terminal output
    # {
    #     'output':'''wlp1s0    Scan completed :
    #   Cell 01 - Address: A0:3D:6F:26:77:8E
    #             Channel:144
    #             Frequency:5.72 GHz
    #             Quality=43/70  Signal level=-67 dBm  
    #             Encryption key:on
    #             ESSID:"ucrwpa"
    #             Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
    #             Mode:Master
    #   Cell 02 - Address: A0:3D:6F:26:77:82
    #             Channel:1
    #             Frequency:2.412 GHz (Channel 1)
    #             Quality=43/70  Signal level=-67 dBm  
    #             Encryption key:on
    #             ESSID:"eduroam"
    #             Bit Rates:18 Mb/s; 24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
    #             Mode:Master''',
    #     'error':''
    # }
```

#### getAPinfo()
```
# Description:
    # Method returns all (or chosen) available access points (in range).
    # Takes 2 optional parameters: 
    #   'networks' (array): 
    #       Lists all ssid's of concern. Will return only the available access 
    #       points listed here. If not provided, will return ALL access-points in range.        
    #   'sudo' (bool): 
    #       Whether of not method should use sudo privileges. If user uses sudo
    #       privileges, the network manager will be refreshed and will return 
    #       a fresh list of access-points available. If sudo is not provided, 
    #       a cached list will be returned. Cached list gets updated periodically.
# -----------------------------------------------
# Input: (Parsed array of cell dictionaries)
    # networks = (array of network names)
    # ['ucrwpa','dd-wrt']
    # sudo = True || False
# -----------------------------------------------
# Returns: (Array of dictionaries)
    # [
    #     {
    #         'ssid':'ucrwpa',
    #         'quality':'43/70',
    #         'signal':'-67'
    #     },
    #     {
    #         'ssid':'dd-wrt',
    #         'quality':'30/70',
    #         'signal':'-42'
    #     }
    # ] 
```
### RSSI_Localizer methods
#### getDistanceFromAP()
```
# Description:
    # Uses the log model to compute an estimated dstance(di) from node(i)
# -------------------------------------------------------
# Input: 
    # accessPoint: dicitonary holding accesspoint info.
    # {
    #     'signalAttenuation': 3, 
    #     'location': {
    #         'y': 1, 
    #         'x': 1
    #     }, 
    #     'reference': {
    #         'distance': 4, 
    #         'signal': -50
    #     }, 
    #     'name': 'dd-wrt'
    # }
    # signalStrength: -69
# -------------------------------------------------------
# output: 
    # accessPoint: dicitonary holding accesspoint info.
    # {
    #     'signalAttenuation': 3, 
    #     'location': {
    #         'y': 1, 
    #         'x': 1
    #     }, 
    #     'reference': {
    #         'distance': 4, 
    #         'signal': -50
    #     }, 
    #     'name': 'dd-wrt'
    # }
    # signalStrength: -69,
    # distance: 2
```
#### getDistancesForAllAPs()
```
# Description:
    # Makes use of 'getDistanceFromAP' to iterate through all 
    # accesspoints being used in localization and obtains the 
    # distance from each one of them.
# ------------------------------------------------
# Input:
    # signalStrengths:
    # [siganl1, siganl2, siganl3]
    # [-42, -53, -77]
# ------------------------------------------------
# Output:
    # [
    #     {
    #         'distance': 4,
    #         'x': 2,
    #         'y': 3
    #     },
    #     {
    #         'distance': 7,
    #         'x': 2,
    #         'y': 5
    #     },
    #     {
    #         'distance': 9,
    #         'x': 7,
    #         'y': 3
    #     }
    # ]
```
#### getNodePosition
```
# Description:
    # Combines 'getDistancesForAllAPs', 'createMatrics',
    # and 'computerPosition' to get the 'X' vector that
    # contains our unkown (x,y) position.
# ----------------------------------------
# Input:
    # signalStrengths
    # [-44, -32 , -63]
# ----------------------------------------
# Output:
    # x
    # [2, 3]
```

## Sample Usage

The following example shows how to use the RSSI_Scan and RSSI_Localizer classes, within the rssi module.

### Initialize RSSI_Scan

This class helps us scan for all available access points, within reach.
User must supply a network interface name, at initialization.
i.e wlan0, docker0, wlp1s0
```
import rssi

interface = 'wlp1s0'
rssi_scanner = rssi.RSSI_Scan(interface)
```
### Scan for access points

#### Scan for specific access points
```
import rssi

interface = 'wlp1s0'
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ['dd-wrt','linksys']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.
ap_info = rssi_scanner.getAPinfo(networks=ssids, sudo=True)

print(ap_info)

# prints
# [
#     {
#         'ssid':'ucrwpa',
#         'quality':'43/70',
#         'signal':'-67'
#     },
#     {
#         'ssid':'dd-wrt',
#         'quality':'30/70',
#         'signal':'-42'
#     }
# ]
```
#### Scan for all access points
```
import rssi

interface = 'wlp1s0'
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ['dd-wrt','linksys']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.
ap_info = rssi_scanner.getAPinfo(sudo=True)

print(ap_info)

# prints
# [
#     {
#         'ssid':'ucrwpa',
#         'quality':'43/70',
#         'signal':'-67'
#     },
#     {
#         'ssid':'dd-wrt',
#         'quality':'30/70',
#         'signal':'-42'
#     },
#     {
#         'ssid':'rosNet',
#         'quality':'30/70',
#         'signal':'-42'
#     },
#     {
#         'ssid':'openNetw',
#         'quality':'30/70',
#         'signal':'-42'
#     }
# ] 
```

### Initialize the RSSI-based localizer
#### RSSI_Localizer
```
# Use:
    # from rssi import RSSI_Localizer
    # rssi_localizer_instance = RSSI_Localizer(accessPoints=accessPoints)
# -------------------------------------------------------
# Description:
    # This class helps a user implement rssi-based localization.
    # The algorithm assumes the logarithmic distance-path-loss model
    # And assumes a minimum of 3 (or more) access points.
# -------------------------------------------------------
# Input:
    # accessPoints: Array holding accessPoint dictionaries.
    #               The order of the arrays supplied will retain
    #               its order, throughout the entire execution.
    # [{
    #     'signalAttenuation': 3, 
    #     'location': {
    #         'y': 1, 
    #         'x': 1
    #     }, 
    #     'reference': {
    #         'distance': 4, 
    #         'signal': -50
    #     }, 
    #     'name': 'dd-wrt'
    # },
    # {
    #     'signalAttenuation': 4, 
    #     'location': {
    #         'y': 1, 
    #         'x': 7
    #     }, 
    #     'reference': {
    #         'distance': 3, 
    #         'signal': -41
    #     }, 
    #     'name': 'ucrwpa'
    # }]
```
#### Estimate distance from access point
```
from rssi import RSSI_Localizer
rssi_localizer_instance = RSSI_Localizer()

accessPoint = {
     'signalAttenuation': 3, 
     'location': {
         'y': 1, 
         'x': 1
     }, 
     'reference': {
         'distance': 4, 
         'signal': -50
     }, 
     'name': 'dd-wrt'
}
signalStrength = -69

distance = rssi_localizer_instance.getDistanceFromAP(accessPoint, signalStrength)
print(distance)

# prints
# {
#     'signalAttenuation': 3, 
#     'location': {
#         'y': 1, 
#         'x': 1
#     }, 
#     'reference': {
#         'distance': 4, 
#         'signal': -50
#     }, 
#     'name': 'dd-wrt',
#     'distance': 2
# }
```

#### Estimate distances form all access points
```
Same as the exmaple above, except accessPoints 
need to be fed into the funciton inside of list.

The function will also return the same output as above in a list.

List order is persistent.
```

#### Perform RSSI-based, self-localization
```
Assuming RSSI_Scan and RSSI_Localizer have already been initialized.
ap_info = rssi.getAPinfo(networks=ssids, sudo=True)
rssi_values = [ap['signal'] for ap in ap_info]
position = localizer.getNodePosition(rssi_values)
print(position)

# prints a 1-D array holding [x,y]
```

## Built With

This package remained incredibly light. The only dependency outside of native Python packages is 'NumPy'.
* [Numpy](https://www.scipy.org/scipylib/download.html) - The fundamental package for scientific computing with Python.

## Contributing

All contributions are welcome! This package was created because of the neccesity for an easy to use module, featuring great documentation, that scales for all uses. All comments, requests, and and recomendations are welcome.

## Authors

* **Juan Antonio Villagomez** - *Developer* - [jvillagomez](https://github.com/jvillagomez)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to Xiuyan Zhu and Yuan Feng, for their publication on RSSI-based indoor localization.
* Shout out to Akila Ganlath PhD at UC Riverside. Without you needing RSSI localization for your robot, I would not have mde this package.
