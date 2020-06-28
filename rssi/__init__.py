name = "rssi"

from subprocess import Popen, PIPE # Used to run native OS commads in python wrapped subproccess
import numpy # Used for matrix operations in localization algorithm
from sys import version_info # Used to check the Python-interpreter version at runtime

# RSSI_Scan
    # Use:
        # from rssi import RSSI_Scan
        # rssi_scan_instance = RSSI_Scan('network_interface_name) 
    # -------------------------------------------------------
    # Description:
        # Allows a user to query all available accesspoints available.
        # User has the option of define a specific set of access 
        # points to query.
    # -------------------------------------------------------
    # Input: interface name
        # [ie. network interface names: wlp1s0m, docker0, wlan0] 
class RSSI_Scan(object):
    # Allows us to declare a network interface externally.
    def __init__(self, interface):
        self.interface = interface

    # getRawNetworkScan
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
    def getRawNetworkScan(self, sudo=False):
        # Scan command 'iwlist interface scan' needs to be fed as an array.
        if sudo:
            scan_command = ['sudo','iwlist',self.interface,'scan']
        else:
            scan_command = ['iwlist',self.interface,'scan']
        # Open a subprocess running the scan command.
        scan_process = Popen(scan_command, stdout=PIPE, stderr=PIPE)
        # Returns the 'success' and 'error' output.
        (raw_output, raw_error) = scan_process.communicate() 
        # Block all execution, until the scanning completes.
        scan_process.wait()
        # Returns all output in a dictionary for easy retrieval.
        return {'output':raw_output,'error':raw_error}

    # getSSID
        # Description:
            # Parses the 'SSID' for a given cell.
        # -----------------------------------------------
        # Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns:
            # 'ucrwpa'
    @staticmethod
    def getSSID(raw_cell):
        ssid = raw_cell.split('ESSID:"')[1]
        ssid = ssid.split('"')[0]
        return ssid

    # getQuality
        # Description:
            # Parses 'Quality level' for a given cell.
        # -----------------------------------------------
        # Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns:
            # '43/70'
    @staticmethod
    def getQuality(raw_cell):
        quality = raw_cell.split('Quality=')[1]
        quality = quality.split(' ')[0]
        return quality

    # getSignalLevel
        # Description:
            # Parses 'Signal level' for a given cell.
            # Measurement is in 'dBm'.
        # -----------------------------------------------
        # Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns: (string)
            # '-67'    
    @staticmethod
    def getSignalLevel(raw_cell):
        signal = raw_cell.split('Signal level=')[1]
        signal = int(signal.split(' ')[0])
        return signal

    # getMacAddress
        # Description:
            # Method returns the MAC address of the AP
        # -----------------------------------------------
        #   Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns: (string)
            #   'A0:3D:6F:26:77:8E'
    @staticmethod
    def getMacAddress(raw_cell):
        mac = raw_cell.split('Address: ')[1]
        mac = mac.split(' ')[0]
        mac = mac.strip()
        return mac

    # parseCell
        # Description:
            # Takes a raw cell string and parses it into a dictionary.
        # -----------------------------------------------
        # Input: (Raw string)
            # '''01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master'''
        # -----------------------------------------------
        # Returns:
            # {
            #     'ssid':'ucrwpa',
            #     'quality':'43/70',
            #     'signal':'-67'
            # }    
    def parseCell(self, raw_cell):
        cell = {
            'ssid': self.getSSID(raw_cell),
            'quality': self.getQuality(raw_cell),
            'signal': self.getSignalLevel(raw_cell),
            'mac': self.getMacAddress(raw_cell)
        }
        return cell

    # formatCells
        # Description:
            # Every network listed is considered a 'cell.
            # This function parses each cell into a dictionary.
            # Returns list of dictionaries. Makes use of 'parseCell'.
            # If not networks were detected, returns False.
        # -----------------------------------------------
        # Input: (Raw terminal string)
            # '''01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
            # 02 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=30/70  Signal level=-42 dBm  
            # Encryption key:on
            # ESSID:"dd-wrt"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master'''
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
    def formatCells(self, raw_cell_string):
        raw_cells = raw_cell_string.split('Cell') # Divide raw string into raw cells.
        raw_cells.pop(0) # Remove unneccesary "Scan Completed" message.
        if(len(raw_cells) > 0): # Continue execution, if atleast one network is detected.
            # Iterate through raw cells for parsing.
            # Array will hold all parsed cells as dictionaries.
            formatted_cells = [self.parseCell(cell) for cell in raw_cells]
            # Return array of dictionaries, containing cells.
            return formatted_cells
        else:
            print("Networks not detected.")
            return False
        # TODO implement function in ndoe to process this boolean (False)

    # filterAccessPoints
        # Description:
            # If the 'networks' parameter is passed to the 'getAPinfo'
            # function, then this method will filter out all irrelevant 
            # access-points. Access points specified in 'networks' array 
            # will be returned (if available).
        # -----------------------------------------------
        # Input: (Parsed array of cell dictionaries)
            # all_access_points = 
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
            #         'ssid':'linksys',
            #         'quality':'58/70',
            #         'signal':'-24'
            #     }
            # ] 
            # network_names = (array of network names)
            # ['ucrwpa','dd-wrt']
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
    @staticmethod
    def filterAccessPoints(all_access_points, network_names):
        focus_points = [] # Array holding the access-points of concern.
        # Iterate throguh all access-points found.
        for point in all_access_points:
            # Check if current AP is in our desired list.
            if point['ssid'] in network_names:
                focus_points.append(point)
        return focus_points
        # TODO implement something incase our desired ones were not found
 
    # getAPinfo
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
    def getAPinfo(self, networks=False, sudo=False):
        # TODO implement error callback if error is raise in subprocess
        # Unparsed access-point listing. AccessPoints are strings.
        raw_scan_output = self.getRawNetworkScan(sudo)['output']
        if version_info.major == 3:
            raw_scan_output = raw_scan_output.decode('utf-8')
        # Parsed access-point listing. Access-points are dictionaries.
        all_access_points = self.formatCells(raw_scan_output)
        # Checks if access-points were found.
        if all_access_points:
            # Checks if specific networks were declared.
            if networks:
                # Return specific access-points found.
                return self.filterAccessPoints(all_access_points, networks)
            else:
                # Return ALL access-points found.
                return all_access_points
        else:
            # No access-points were found. 
            return False

# RSSI_Localizer
    # Use:
        # from rssi import RSSI_Localizer
        # rssi_localizer_instance = RSSI_Localizer()
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
class RSSI_Localizer(object):
    # Allows us to fetch for networks/accessPoints externally.
    # Array of access points must be formatted.
    # 'self.count' parameter is computed internally to aid in 
    # scaling of the algorithm.
    def __init__(self,accessPoints):
        self.accessPoints = accessPoints
        self.count = len(accessPoints)

    # getDistanceFromAP
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
            #     'name': 'dd-wrt',
            #     'distance': 2
            # }
    @staticmethod
    def getDistanceFromAP(accessPoint, signalStrength):
        beta_numerator = float(accessPoint['reference']['signal']-signalStrength)
        beta_denominator = float(10*accessPoint['signalAttenuation'])
        beta = beta_numerator/beta_denominator
        distanceFromAP = round(((10**beta)*accessPoint['reference']['distance']),4)
        accessPoint.update({'distance':distanceFromAP})
        return accessPoint
    
    # TODO fix this because theres two consecutive for loops. 
    # One that runs to fefd signal strengths to this function, 
    # a second consecutive loop inside the function.

    # getDistancesForAllAPs
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
    def getDistancesForAllAPs(self, signalStrengths):
        apNodes = []
        for i in range(len(self.accessPoints)):
            ap = self.accessPoints[i] 
            distanceFromAP = self.getDistanceFromAP(
                ap,
                signalStrengths[i]
            )
            apNodes.append({
                'distance': distanceFromAP['distance'],
                'x': ap['location']['x'],
                'y': ap['location']['y']
            })
        return apNodes
    
    # createMatrices
        # Description:
            # Creates tehmatrices neccesary to use the least squares method
            # in order to mnimize the error (error=|realDistance-estimatedDistance|). 
            # Assuming 'n' number of nodes and d(m) is the distance(d) from node (m).
            # AX = B, where X is our estimated location.
            # A = [
            #     2(x(i)-xn)    2(y(i)-yn)
            #     2(x(i+1)-xn)  2(y(i+1)-yn)
            #     ...           ...
            #     2(x(n-1)-xn)  2(y(n-1)-yn)
            # ]
            # B = [
            #     x(i)^2 + y(i)^2 - x(n)^2 + y(n)^2 - d(i)^2 + d(n)^2
            #     x(i+1)^2 + y(i+1)^2 - x(n)^2 + y(n)^2 - d(i+1)^2 + d(n)^2
            #     ...
            #     x(n-1)^2 + y(n-1)^2 - x(n)^2 + y(n)^2 - d(n-1)^2 + d(n)^2
            # ]
        # ----------------------------------------
        # Input:
            # accessPoints
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
        # ----------------------------------------
        # Output:
            # A = [
            #     2(2-7)    2(3-3)
            #     2(2-7)  2(5-3)
            # ]
            # B = [
            #     2^2 + 3^2 - 7^2 + 3^2 - 4^2 + 9^2
            #     2^2 + 5^2 - 7^2 + 3^2 - 7^2 + 9^2
            # ]
    def createMatrices(self, accessPoints):
        # Sets up that te matrics only go as far as 'n-1' rows,
        # with 'n being the # of access points being used.
        n_count = self.count-1
        # initialize 'A' matrix with 'n-1' ranodm rows.
        a = numpy.empty((n_count,2))
        # initialize 'B' matrix with 'n-1' ranodm rows.
        b = numpy.empty((n_count,1))
        # Define 'x(n)' (x of last accesspoint)
        x_n = accessPoints[n_count]['x'] 
        # Define 'y(n)' (y of last accesspoint)
        y_n = accessPoints[n_count]['y']
        # Define 'd(n)' (distance from of last accesspoint)
        d_n = accessPoints[n_count]['distance']
        # Iteration through accesspoints is done upto 'n-1' only
        for i in range(n_count):
            ap = accessPoints[i]
            x, y, d = ap['x'], ap['y'], ap['distance']
            a[i] = [2*(x-x_n), 2*(y-y_n)]
            b[i] = [(x**2)+(y**2)-(x_n**2)-(y_n**2)-(d**2)+(d_n**2)]
        return a, b
    
    # computePosition
        # Description:
            # Performs the 'least squares method' matrix operations 
            # neccessary to get the 'x' and 'y' of the unknown 
            # beacon's position.
            # X = [(A_transposed*A)^-1]*[A_transposed*B]
        # ----------------------------------------
        # Input:
            # A = [
            #     0   0
            #     0  -4
            # ]
            # B = [
            #     4 + 9 - 49 + 9 - 16 + 81  => 38
            #     4 + 25 - 49 + 9 - 49 + 81 => 21
            # ]
        # ----------------------------------------
        # Output:
            # x
            # [
            #     2,
            #     3
            # ]
    @staticmethod
    def computePosition(a, b):
        # Get 'A_transposed' matrix
        at = numpy.transpose(a)
        # Get 'A_transposed*A' matrix
        at_a = numpy.matmul(at,a)
        # Get '[(A_transposed*A)^-1]' matrix
        inv_at_a = numpy.linalg.inv(at_a)
        # Get '[A_transposed*B]'
        at_b = numpy.matmul(at,b)
        # Get '[(A_transposed*A)^-1]*[A_transposed*B]'
        # This holds our position (xn,yn)
        x = numpy.matmul(inv_at_a,at_b) 
        return x

    # getNodePosition
        # Description:
            # Combines 'getDistancesForAllAPs', 'createMatrics',
            # and 'computerPosition' to get the 'X' vector that
            # contains our unkown (x,y) position.
        # ----------------------------------------
        # Input:
            # signalStrengths
            # [4, 2 , 3]
        # ----------------------------------------
        # Output:
            # x
            # [2, 3]
    def getNodePosition(self, signalStrengths):
        apNodes = self.getDistancesForAllAPs(signalStrengths)
        a, b = self.createMatrices(apNodes) 
        position = self.computePosition(a, b)
        # print(a)
        # print(b)
        return position
