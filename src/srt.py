import datetime

class SRTWriter:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.current_time = 0.0  # 秒単位

    def add(self, text, duration):
        """
        セリフを追加する
        :param text: 字幕の内容（文字列）
        :param duration: 再生時間（秒数）
        """
        start_time = self._seconds_to_timestamp(self.current_time)
        end_time = self._seconds_to_timestamp(self.current_time + duration)
        self.entries.append((start_time, end_time, text))
        self.current_time += duration

    def write(self):
        """
        SRTファイルを書き出す
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            for i, (start, end, text) in enumerate(self.entries, 1):
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

    def _seconds_to_timestamp(self, seconds):
        """
        秒数をSRT形式のタイムスタンプに変換
        """
        seconds = round(seconds, 3)
        td = datetime.timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        ms = int((td.total_seconds() - total_seconds) * 1000)
        h, rem = divmod(total_seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
