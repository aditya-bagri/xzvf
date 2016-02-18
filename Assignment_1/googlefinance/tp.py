from googlefinance import getQuotes
import json
print json.dumps(getQuotes('ATX'), indent=2)
#print json.dumps(getQuotes("TCS"), indent=2, index="BSE")
