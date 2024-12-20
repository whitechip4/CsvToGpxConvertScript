import pandas as pd
import sys
import os


# change const below according to your csv header name
_DATE_COLUMN_NAME = "date"
_TIME_COLUMN_NAME = "time"
_LAT_COLUMN_NAME = "lat"
_LON_COLUMN_NAME ="lng"
_ALTITUDE_COLUMN_NAME = "alt"

# property for xml
auther_name = "your name"

def convert_csv_to_pdf(csv_file_path:str):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)
    output_file_path = csv_file_path.replace('.csv', '.gpx')

    # change date format
    df[_DATE_COLUMN_NAME] = pd.to_datetime(df[_DATE_COLUMN_NAME]).dt.strftime('%Y-%m-%d')
    init_date = df[_DATE_COLUMN_NAME][0]
    init_time = df[_TIME_COLUMN_NAME][0]
    init_date_time = init_date +'T'+init_time +'Z'
    print (init_date_time)

    # get min max
    minlat = df[_LAT_COLUMN_NAME].min()
    maxlat = df[_LAT_COLUMN_NAME].max()
    minlon = df[_LON_COLUMN_NAME].min()
    maxlon = df[_LON_COLUMN_NAME].max()
    print(minlat,minlon,maxlat,maxlon)

    # reference:  gpx data exported by qoocam3 ultra
    with open(output_file_path, 'w', encoding='utf-8') as wfile:
        # TODO refactoring
        wfile.write(f'<?xml version="1.0" encoding="utf-8"?><gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.0" creator="{auther_name}">\n')
        wfile.write('  <metadata>\n')
        wfile.write(f'    <time>{init_date_time}</time>\n')
        wfile.write(f'    <bounds minlat="{minlat}" maxlat="{maxlat}" minlon="{minlon}" maxlon="{maxlon}"/>\n',)
        wfile.write('  </metadata>\n')

        wfile.write('  <trk>\n')
        wfile.write('    <name>M5stack GNSS Data</name>\n')
        wfile.write('    <trkseg>\n')

        for index, row in df.iterrows():
            wfile.write(f'      <trkpt lat="{row[_LAT_COLUMN_NAME]}" lon="{row[_LON_COLUMN_NAME]}">\n')
            wfile.write(f'        <ele>{row[_ALTITUDE_COLUMN_NAME]}</ele>\n')
            wfile.write(f'        <time>{row[_DATE_COLUMN_NAME]}T{row[_TIME_COLUMN_NAME ]}Z</time>\n')
            wfile.write(f'      </trkpt>\n')

        wfile.write('    </trkseg>\n')
        wfile.write('  </trk>\n')
        wfile.write('</gpx>')

if __name__ == '__main__': 
    # argument check
    if (len(sys.argv) != 2):
        print("Usage : input filepath")
        exit(1)

    # file check
    csv_file_path = sys.argv[1]
    if not os.path.exists(csv_file_path):
        print("File not found")
        exit(1)
    if not csv_file_path.endswith('.csv'):
        print("Usage : input csv filepath")
        exit(1)
    
    convert_csv_to_pdf(csv_file_path)