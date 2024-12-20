import pandas as pd
import sys
import os

class CsvGpxConverter:
    # change const below according to your csv header name
    DATE_COLUMN_NAME = "date"
    TIME_COLUMN_NAME = "time"
    LAT_COLUMN_NAME = "lat"
    LON_COLUMN_NAME ="lng"
    ALTITUDE_COLUMN_NAME = "alt"

    # property for xml
    auther_name = "your name"

    def convert_csv_to_pdf(self,csv_file_path:str):
        # read csv
        df = pd.read_csv(csv_file_path)
        output_file_path = csv_file_path.replace('.csv', '.gpx')

        # change date format
        df[self.DATE_COLUMN_NAME] = pd.to_datetime(df[self.DATE_COLUMN_NAME]).dt.strftime('%Y-%m-%d')
        init_date = df[self.DATE_COLUMN_NAME][0]
        init_time = df[self.TIME_COLUMN_NAME][0]
        init_date_time = init_date +'T'+init_time +'Z'
        print (init_date_time)

        # get min max
        minlat = df[self.LAT_COLUMN_NAME].min()
        maxlat = df[self.LAT_COLUMN_NAME].max()
        minlon = df[self.LON_COLUMN_NAME].min()
        maxlon = df[self.LON_COLUMN_NAME].max()
        print(minlat,minlon,maxlat,maxlon)

        # reference: gpx data exported by qoocam3 ultra
        with open(output_file_path, 'w', encoding='utf-8') as wfile:
            # TODO refactoring
            wfile.write(f'<?xml version="1.0" encoding="utf-8"?><gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.0" creator="{self.auther_name}">\n')
            wfile.write('  <metadata>\n')
            wfile.write(f'    <time>{init_date_time}</time>\n')
            wfile.write(f'    <bounds minlat="{minlat}" maxlat="{maxlat}" minlon="{minlon}" maxlon="{maxlon}"/>\n',)
            wfile.write('  </metadata>\n')

            wfile.write('  <trk>\n')
            wfile.write('    <name>M5stack GNSS Data</name>\n')
            wfile.write('    <trkseg>\n')

            for _index, row in df.iterrows():
                wfile.write(f'      <trkpt lat="{row[self.LAT_COLUMN_NAME]}" lon="{row[self.LON_COLUMN_NAME]}">\n')
                wfile.write(f'        <ele>{row[self.ALTITUDE_COLUMN_NAME]}</ele>\n')
                wfile.write(f'        <time>{row[self.DATE_COLUMN_NAME]}T{row[self.TIME_COLUMN_NAME ]}Z</time>\n')
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
    
    converter = CsvGpxConverter()
    converter.convert_csv_to_pdf(csv_file_path)