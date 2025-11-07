import os
import csv
import argparse
from srt import SRTWriter

outputdir = "./output/"

def process_csv(input_path, total_time_str, output_path):

    srt = SRTWriter(output_path)

    total_seconds = time_to_seconds(total_time_str)
    rows = []

    with open(input_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            rows.append(row)

    rows.sort(key=lambda x: int(x[0]))
    for i in range(len(rows)):
        text = rows[i][4]
        start_time = time_to_seconds(rows[i][1])

        if i < len(rows) - 1:
            end_time = time_to_seconds(rows[i + 1][1])
        else:
            end_time = total_seconds  # 最後の行は動画全体時間

        duration = end_time - start_time
        if duration < 0:
            duration = 0  # 念のため

        srt.add(text, duration)
    
    srt.write()

def time_to_seconds(timestr):
    # "00:00:01.8000000" → 秒(float)
    h, m, s = timestr.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VOICEVOX CSV → SRT 変換ツール")
    parser.add_argument("--input", required=True, help="入力CSVファイルのパス")
    parser.add_argument("--total", required=True, help="動画全体の長さ（例: 00:00:10.000）")
    parser.add_argument("--output", default="output/output.srt", help="出力SRTファイルのパス")
    args = parser.parse_args()
    process_csv(args.input, args.total, args.output)
    