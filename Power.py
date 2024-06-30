import csv

class Power():
    def __init__(self, csvFilePath):
        csv_file = csvFilePath

        data = {}

        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)

            data[header[0]] = header[1:]
            for row in reader:
                data[row[0]] = row[1:]

        self.dfdata = data
    
    #returns the date on which the usage is the max based on power_type
    def peak_date(self,power_type):
        res = ""
        maxEnergy = 0.0
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        for i in range (len(indicatorData)):
            if float(indicatorData[i]) > maxEnergy:
                maxEnergy = float(indicatorData[i])
                res = self.dfdata["Indicators"][i]

        return res
    
    #return max value
    def max(self, power_type):
        maxEnergy = 0.0
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        for i in range (len(indicatorData)):
            if float(indicatorData[i]) > maxEnergy:
                maxEnergy = float(indicatorData[i])

        return maxEnergy
    
    #returns min value
    def min(self, power_type):
        minEnergy = 1<<63
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        for i in range (len(indicatorData)):
            if float(indicatorData[i]) != 0 and float(indicatorData[i]) < minEnergy:
                minEnergy = float(indicatorData[i])

        return minEnergy
    
    #return unique counts except 0
    def count(self, power_type):
        cnt = 0
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        for i in range (len(indicatorData)):
            if float(indicatorData[i]) != 0:
                cnt+=1

        return cnt

    #return 25th percentile
    def percentile25(self, power_type):
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        pos = len(indicatorData)
        return sorted(indicatorData)[pos//4]
    
    #returns 50% percentile
    def median(self, power_type):
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        pos = len(indicatorData)
        return sorted(indicatorData)[pos//2]
    
    #returns 75%percentile
    def percentile75(self, power_type):
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        pos = len(indicatorData)
        return sorted(indicatorData)[pos*3//4]
    
    #returns mean 
    def mean(self, power_type):
        sum = 0
        indicatorData = self.dfdata["Output of "+power_type+", Current Period(100 million kwh)"]
        for data in indicatorData:
            sum += float(data)

        return format(sum/len(indicatorData), ".2f")
        
    # provides various statistics about the data based on power_type
    def desc_stats(self, power_type):
        return[
            self.max(power_type),
            self.min(power_type),
            self.count(power_type),
            self.percentile25(power_type),
            self.median(power_type),
            self.percentile75(power_type),
            self.mean(power_type)
        ]
    
    # return contribution of energy of each type on particular date
    def contribution(self, date):
        # The end date is being stores in consideration to 
        # leap year. Therefore, while quering the API,
        # take care of the leap year

        pos = -1
        for i in range(len(self.dfdata["Indicators"])):
            if self.dfdata["Indicators"][i] == "\""+date+"\"":
                pos = i
                break

        if pos == -1:
            return "Invalid Date"
        
        thermalPower = float(self.dfdata["Output of Thermal Power, Current Period(100 million kwh)"][pos])
        hydroElectricPower = float(self.dfdata["Output of Hydro-electric Power, Current Period(100 million kwh)"][pos])
        nuclearPower = float(self.dfdata["Output of Nuclear Power, Current Period(100 million kwh)"][pos])
        windPower = float(self.dfdata["Output of Wind Power, Current Period(100 million kwh)"][pos])
        solarPower = float(self.dfdata["Output of Solar Power, Current Period(100 million kwh)"][pos])
        
        sum = thermalPower+hydroElectricPower+nuclearPower+windPower+solarPower

        return [
            format(thermalPower/sum*100, ".2f"),
            format(hydroElectricPower/sum*100, ".2f"), 
            format(nuclearPower/sum*100, ".2f"), 
            format(windPower/sum*100, ".2f"), 
            format(solarPower/sum*100, ".2f")
        ]

    

obj = Power("./output.csv")
print("peak data:", obj.peak_date("Solar Power"))
print("Solar Power", obj.desc_stats("Solar Power"))
print("Contribution",obj.contribution("2024-05-31"))
