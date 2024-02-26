#=================================================CODE==================================================
from typing import *
import csv

MOVIE_NAME = "Dune2"


def int_ranges_to_str(numbers) -> list[str]:
    ranges = [[numbers[0]]]

    for n in numbers[1:]:
        if n - ranges[-1][-1] == 1:
            ranges[-1].append(n)
        else:
            ranges.append([n])

    return ['-'.join(map(str, [r[0], r[-1]])) if len(r) > 1 else str(r[0]) for r in ranges]


def filter_frames(frames: List[str]) -> List[int]:
    """Filter out <null> and <err> values and transform each valid frame to an int"""

    frames = [n for n in frames if n not in ['<null>', '<err>']]
    return [int(n) for n in frames]


def read_baselight(path: str) -> Dict[str, List[str]]:
    baselight_file = open(path, 'r')
    content = {}
    for line in baselight_file.readlines():
        dir = line.split(' ')[0]
        frames = line.strip().split(' ')[1:]
        filtered = filter_frames(frames)
        processed = int_ranges_to_str(filtered)
        if dir not in content:
            content[dir] = processed
        else:
            content[dir] += processed
    baselight_file.close()
    return content


def dir_str_to_list(dir: str) -> List[str]:
    return dir.split('/')[1:]


def dir_list_to_str(dir: List[str]) -> str:
    return '/'.join(dir)


def match_dir(dir1: str, dir2: str) -> bool:
    return dir1[dir1.index(MOVIE_NAME):] == dir2[dir2.index(MOVIE_NAME):]


class WorkOrder:
    def __init__(self, path: str) -> None:
        self.read_file(path)

    def read_file(self, path: str) -> None:
        file = open(path, 'r')
        file_content = file.readlines()

        self.title = file_content[0].strip()
        self.producer = file_content[2].strip().split(':')[1].strip()
        self.operator = file_content[3].strip().split(':')[1].strip()
        self.job = file_content[4].strip().split(':')[1].strip()
        self.frames = {}
        # frames = {dir -> ranges of frames}

        curr = 8
        while file_content[curr].strip() != '':
            self.frames[file_content[curr].strip()] = ""
            curr += 1
        curr += 2
        self.notes = file_content[curr].strip()

    def test(self):
        print(self.title)
        print(self.producer)
        print(self.operator)
        print(self.job)
        print(self.notes)
        for (k, v) in self.frames.items():
            print(f"{k}: {v}")

    def import_baselight_frames(self, baselight_content: Dict[str, List[str]]) -> None:
        for work_dir in self.frames.keys():
            for baselight_dir in baselight_content.keys():
                if match_dir(work_dir, baselight_dir):
                    self.frames[work_dir] = baselight_content[baselight_dir]


baselight_content = read_baselight('./Baselight_export.txt')


W = WorkOrder("./Xytech.txt")
W.import_baselight_frames(baselight_content)
W.test()


def export_to_csv(wo: WorkOrder) -> None:
    with open(f"{wo.title}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Producer', 'Operator', 'Job', 'Notes'])
        writer.writerow([wo.producer, wo.operator, wo.job, wo.notes])
        writer.writerow([])
        writer.writerow([])
        writer.writerow(['Locations', 'Frames to fix'])
        for (k, v) in wo.frames.items():
            for frame in v:
                writer.writerow([k, frame])
        file.close()


export_to_csv(W)
