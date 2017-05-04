import datetime
import billboard
import csv

#TO COLLECT SONG DATA (Song,Artist) FROM BILLBOARD FOR LAST 10 WEEKS

s = '2017-04-22'
charts=[]
uniqueSongs = {}

for i in range(0,10):
	d = datetime.datetime.strptime(s, '%Y-%m-%d') + datetime.timedelta(weeks=-i)
	songsData = billboard.ChartData('hot-100', quantize=True, date=d.strftime('%Y-%m-%d'))
	for i in range(0,100):
		title = songsData[i].title
		if title not in uniqueSongs:
			uniqueSongs[title] = songsData[i].artist

with open('/Users/Vaidehi/Desktop/billboardData.csv', 'wb') as csv_file:
	writer = csv.writer(csv_file)
	for key, value in uniqueSongs.items():
		writer.writerow([key] + [value])
	csv_file.close()
