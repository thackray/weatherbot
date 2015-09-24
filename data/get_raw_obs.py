import os

os.system("cd data")
for year in range(1997,2007):
    for month in range(1,13):
        os.system("wget http://www.ncdc.noaa.gov/orders/qclcd/%s%.2d.tar.gz"%(year,month))
        os.system("tar -C obs -zxvf %s%.2d.tar.gz"%(year,month))
        os.system("rm %s%.2d.tar.gz"%(year,month))
year = 2007
for month in range(1,8):
    os.system("wget http://www.ncdc.noaa.gov/orders/qclcd/%s%.2d.tar.gz"%(year,month))
    os.system("tar -C obs -zxvf %s%.2d.tar.gz"%(year,month))
    os.system("rm %s%.2d.tar.gz"%(year,month))
#transition happens 200707
for month in range(8,13):
    os.system("wget http://www.ncdc.noaa.gov/orders/qclcd/QCLCD%s%.2d.zip"%(year,month))
    os.system("unzip QCLCD%s%.2d.zip -d obs"%(year,month))
    os.system("rm QCLCD%s%.2d.zip"%(year,month))

for year in range(2008,2015):
    for month in range(1,13):
        os.system("wget http://www.ncdc.noaa.gov/orders/qclcd/QCLCD%s%.2d.zip"%(year,month))
        os.system("unzip QCLCD%s%.2d.zip -d obs"%(year,month))
        os.system("rm QCLCD%s%.2d.zip"%(year,month))
