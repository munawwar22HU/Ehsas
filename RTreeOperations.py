import pandas as pd
import geocoder
import math
from RR import *


class TreeOp:
    def __init__(self, path=None):

        # The path is the path of the csv file. Call this function to create the R-Trees
        # Will Create R-Entries and then those entries will be search
        # X is the longitude, Y is the Latitude
        self.tree = RTree()
        self.Area = dict()
        self.Results = list()
        df = pd.read_csv(path, header=0)
        for i, row in df.iterrows():
            Lat = float(row['Latitude'])
            Lon = float(row['Longitude'])
            g = geocoder.google([Lat, Lon], method='reverse')

            #g = geocoder.google(row['Address']+',Karachi,Sindh,Pakistan')
            a = g.bbox
            x1, y1 = self.convertSphericalToCartesian(
                a["northeast"][0], a["northeast"][1])
            x2, y2 = self.convertSphericalToCartesian(
                a["southwest"][0], a["southwest"][1])
            entry = TreeEntry(([x1, x2], [y1, y2]))

            g = geocoder.google(row['Area']+',Karachi,Sindh,Pakistan')
            a = g.bbox

            x1, y1 = self.convertSphericalToCartesian(
                a["northeast"][0], a["northeast"][1])
            x2, y2 = self.convertSphericalToCartesian(
                a["southwest"][0], a["southwest"][1])
            if row['Area'] not in self.Area:
                self.Area[row['Area']] = ([x1, x2], [y1, y2])
            # ShopID,Name,Address,City,Province,Area,Cell,Landline,Longitude,Latitude,StoreType

            Name = row['Name']
            Address = row['Address']
            Province = row['Province']
            Area = row['Area']
            Cell = row['Cell']
            Landline = row['Landline']
            Latitude = row['Latitude']
            Longitude = row['Longitude']
            StoreType = row['StoreType'].split(";")

            entry.setData(Name, Address, Province, Area, Cell,
                          Landline, Latitude, Longitude, StoreType)
            self.tree.insert(entry)
            self.Results.append(entry)
            if i == 5:
                break

        print(self.tree.Root)

    def getAreas(self):
        # This function will return disctinct dictionary of areas of the file
        # For each Area in the key I will store its bounding box
        return list(self.Area.keys())

    def Search(self, Entity, AreaK, flag):
        # Entity will tell what key what type of store
        # AreaChose will be the key to the dictionary which will then select the file the bounds for searching
        # NearMe is a boolean flag that will tell key Near Me search karni hai

        filter = []
        if flag == False:
            for i in self.Results:
                if Entity in i.StoreType:
                    filter.append(i)
        else:
            serch = self.tree.Search(self.tree.Root, self.Area[AreaK])
            for i in serch:
                if Entity in i.StoreType:
                    filter.append(i)
        return filter

    def convertSphericalToCartesian(self, latitude, longitude):

        # Convert from Degrees to Radians
        latRad = latitude * (math.pi)/180
        lonRad = longitude * (math.pi)/180

        earthRadius = 6367  # Radius in km
        posX = earthRadius * math.cos(latRad) * math.cos(lonRad)
        posY = earthRadius * math.cos(latRad) * math.sin(lonRad)
        return(round(posX, 3), round(posY, 3))
