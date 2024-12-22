## CsvToGpxConvertScript
csvで記録されているGPS,GNSSデータをgoogleマイマップ用の.gpxファイルに変換します。

### CSVファイル
以下の5つのデータを使用します
* date
  * 日付。 string YYYY/MM/dd 形式
* time
  * 時刻。string HH:MM:SS 形式
* lat
  * 緯度。 number。
* lng
  * 緯度。 number。
* alt
  * 高度。 number。 なければゼロ埋めでいいです

ラベルは自由に設定できるため、形式さえ合っていれば問題ないです。

### 備考
* 4MBあたりで分割して出力します。Googleマイマップが5MBまでのGPXにしか対応してないため。
