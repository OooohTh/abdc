Home='/afs/.ist.utl.pt/users/0/4/ist1109904/Desktop/Repository/exercisesfp/Lab5/'
def readfile():
    CountryDict={}
    f=open(Home+'cities.txt','r')
    raline=f.readline()[:-1]
    while raline != '':
        rline=raline.split('|')
        if rline[0] not in CountryDict.keys():
            CountryDict[rline[0]]=[rline[1]]
        else:
            CountryDict[rline[0]].append(rline[1])
        raline=f.readline()[:-1]
    f.close()
    return CountryDict

def writefile(CountryDict):
    f=open(Home+'cities.ord.txt','w')
    CountryList=list(CountryDict.keys())
    CountryList.sort()
    SortedCountryDict={i : CountryDict[i] for i in CountryList}
    print (SortedCountryDict)
    for country in SortedCountryDict:
        SortedCityList=list(SortedCountryDict[country])
        SortedCityList.sort()
        print (SortedCityList)
        SortedCountryDict[country]=SortedCityList
    for country in SortedCountryDict.keys():
        for city in SortedCountryDict[country]:
            f.write(country+'|'+city+'\n')
    f.close()
    

def main():
    a=readfile()
    writefile(a)

main()