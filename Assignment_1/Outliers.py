import math
from pyspark import SparkContext
sc = SparkContext()
import sys

#####################

TEST_MODE=1
LIVE_MODE=0
def test_outlier(mode):
#       a = np.random.randint(-1500, 1500, 2500).astype(np.float64)+np.random.rand(1,2500)
        if mode:
                path = "./Q4_with_data/"
        else:
                path = "./Q4_files/"
#               main()
        reader=csv.DictReader(open('Yahoo_symbols.csv','rb'))
        price_arr=[]
        for row in reader:
                print row
                company=row["COMPANY"]
                symbol=row["SYMBOL"]
                while(1):
                           try:
                                share_name=Share(symbol)
                                if share_name:
                                        break
                           except:
                                time.sleep(1)

#                share_name=Share(symbol)
                filename = path+company+".csv"
                file=open(filename,"r+")
                price_arr=[]
                for line in file:
#                       print line
                    try:
                        price_arr.append(float(str(line).split(',')[1]))
                    except:
                        pass
		val, cleaned = outlier(price_arr)

#####################


def removeOutliers(nums):
    	stats = nums.stats()
    	sig = math.sqrt(stats.variance())
    	cleaned= nums.filter(lambda x: math.fabs(x - stats.mean()) <= 2 * sig)
	return cleaned

def arrOfOutliers(nums):
        stats = nums.stats()
        sig = math.sqrt(stats.variance())
        outliers= nums.filter(lambda x: math.fabs(x - stats.mean()) > 2 * sig)
	return outliers

def outlier(arr):
	nums = sc.parallelize(arr)
	val = sorted(removeOutliers(nums).collect())
	out = sorted(arrOfOutliers(nums).collect())
	return val, out

x = [12,32,11,21,18,19,23,4,11,23,45,67,22,4,98]
val,clean =outlier(x)
print val
print clean
