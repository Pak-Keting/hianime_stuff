from pathlib import Path

def localize_m3u8(m3u8: str, video_path: str) -> str:
    lines = []
    for i in m3u8.split():
        if "https://" in i:
            filename_fixed = Path(i).stem + ".ts"
            lines.append(str(Path(video_path) / filename_fixed))
        else:
            lines.append(i)
    return "\n".join(lines)


def get_segment_links(m3u8: str) -> list:
    return [i for i in m3u8.split() if "https://" in i]


def get_segment_filenames_fixed_extension(m3u8: str) -> list:
    return [Path(i).stem + ".ts" for i in m3u8.split() if "https://" in i]
    



if __name__ == "__main__":
    m3u8 = open('./samples/index-f3-v1-a1.m3u8').read()

    a = localize_m3u8(m3u8,'/dsg/ageha/hbwh/jsxdf/')
    b = get_segment_links(m3u8)
    c = get_segment_filenames_fixed_extension(m3u8)
    print(a)
