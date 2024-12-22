#!python3
import pandas as pd
import sys
import os


class CsvGpxConverter:
    ### private constant
    _DEFAULT_DATE_COLUMN_NAME = "date"
    _DEFAULT_TIME_COLUMN_NAME = "time"
    _DEFAULT_LAT_COLUMN_NAME = "lat"  # latitude
    _DEFAULT_LON_COLUMN_NAME = "lng"  # longitude
    _DEFAULT_ALTITUDE_COLUMN_NAME = "alt"

    _DEFAULT_AUTHER_NAME = "your name"
    _DEFAULT_TITLE = "gnss data"

    __XML_INDENT = ["", "  ", "    ", "      ", "        "]

    def __init__(self):
        self.date_column_name = CsvGpxConverter._DEFAULT_DATE_COLUMN_NAME
        self.time_column_name = CsvGpxConverter._DEFAULT_TIME_COLUMN_NAME
        self.lat_column_name = CsvGpxConverter._DEFAULT_LAT_COLUMN_NAME
        self.lon_column_name = CsvGpxConverter._DEFAULT_LON_COLUMN_NAME
        self.altitude_column_name = CsvGpxConverter._DEFAULT_ALTITUDE_COLUMN_NAME
        self.auther_name = CsvGpxConverter._DEFAULT_AUTHER_NAME
        self.title = CsvGpxConverter._DEFAULT_TITLE

    @property
    def date_column_name(self) -> str:
        return self._date_column_name

    @date_column_name.setter
    def date_column_name(self, value: str):
        self._date_column_name = value

    @property
    def time_column_name(self) -> str:
        return self._time_column_name

    @time_column_name.setter
    def time_column_name(self, value: str):
        self._time_column_name = value

    @property
    def lat_column_name(self) -> str:
        return self._lat_column_name

    @lat_column_name.setter
    def lat_column_name(self, value: str):
        self._lat_column_name = value

    @property
    def lon_column_name(self) -> str:
        return self._lon_column_name

    @lon_column_name.setter
    def lon_column_name(self, value: str):
        self._lon_column_name = value

    @property
    def altitude_column_name(self) -> str:
        return self._altitude_column_name

    @altitude_column_name.setter
    def altitude_column_name(self, value: str):
        self._altitude_column_name = value

    @property
    def auther_name(self) -> str:
        return self._auther_name

    @auther_name.setter
    def auther_name(self, value: str):
        self._auther_name = value

    ### private method
    def _is_csv_file(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        if not file_path.endswith(".csv"):
            return False
        return True

    def _is_csv_file_format_correct(self, df: pd.DataFrame) -> bool:
        required_columns = [
            self.date_column_name,
            self.time_column_name,
            self.lat_column_name,
            self.lon_column_name,
            self.altitude_column_name,
        ]
        for column in required_columns:
            if column not in df.columns:
                return False
        return True

    def _get_column_min_max(self, df: pd.DataFrame, column_name: str) -> tuple:
        return df[column_name].min(), df[column_name].max()

    ### public method
    def convert_csv_to_pdf(self, csv_file_path: str) -> bool:

        if not self._is_csv_file(csv_file_path):
            print(f"{csv_file_path} is not csv file")
            return False

        df = pd.read_csv(csv_file_path)
        is_csv_format_correct = self._is_csv_file_format_correct(df)
        if not is_csv_format_correct:
            print(f"{csv_file_path} label is not matched")
            return False

        try:
            output_file_path = csv_file_path.replace(".csv", ".gpx")
            # change date format
            df[self.date_column_name] = pd.to_datetime(
                df[self.date_column_name]
            ).dt.strftime("%Y-%m-%d")

            init_date = df[self.date_column_name][0]
            init_time = df[self.time_column_name][0]
            init_date_time = init_date + "T" + init_time + "Z"
            print(f"recorded date: {init_date_time}")

            # get min max
            minlat, maxlat = self._get_column_min_max(df, self.lat_column_name)
            minlon, maxlon = self._get_column_min_max(df, self.lon_column_name)
            print(f"lat minmax[{minlat}:{maxlat}], lon minmax [{minlon}:{maxlon}]")

            # reference: gpx data exported by qoocam3 ultra
            with open(output_file_path, "w", encoding="utf-8") as wfile:
                # TODO refactoring
                wfile.write(
                    f'<?xml version="1.0" encoding="utf-8"?><gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.0" creator="{self.auther_name}">\n'
                )
                wfile.write(f"{self.__XML_INDENT[1]}<metadata>\n")
                wfile.write(f"{self.__XML_INDENT[2]}<time>{init_date_time}</time>\n")
                wfile.write(
                    f'{self.__XML_INDENT[2]}<bounds minlat="{minlat}" maxlat="{maxlat}" minlon="{minlon}" maxlon="{maxlon}"/>\n',
                )
                wfile.write(f"{self.__XML_INDENT[1]}</metadata>\n")

                wfile.write(f"{self.__XML_INDENT[1]}<trk>\n")
                wfile.write(f"{self.__XML_INDENT[2]}<name>{self.title}</name>\n")
                wfile.write(f"{self.__XML_INDENT[2]}<trkseg>\n")

                for _index, row in df.iterrows():
                    wfile.write(
                        f'{self.__XML_INDENT[3]}<trkpt lat="{row[self.lat_column_name]}" lon="{row[self.lon_column_name]}">\n'
                    )
                    wfile.write(
                        f"{self.__XML_INDENT[4]}<ele>{row[self.altitude_column_name]}</ele>\n"
                    )
                    wfile.write(
                        f"{self.__XML_INDENT[4]}<time>{row[self.date_column_name]}T{row[self.time_column_name ]}Z</time>\n"
                    )
                    wfile.write(f"{self.__XML_INDENT[3]}</trkpt>\n")

                wfile.write(f"{self.__XML_INDENT[2]}</trkseg>\n")
                wfile.write(f"{self.__XML_INDENT[1]}</trk>\n")
                wfile.write("</gpx>")
        except Exception as e:
            print(f"csv format is not correct {e}")
            return False

        print(
            f"converted completed, exported file is : {os.path.join(os.path.dirname(__file__),output_file_path)}"
        )
        return True


if __name__ == "__main__":
    # argument check
    if len(sys.argv) != 2:
        print("Usage : convert.py [input filepath]")
        exit(1)
    file_path = sys.argv[1]

    converter = CsvGpxConverter()
    converter.convert_csv_to_pdf(file_path)
