import csv
import re

import pandas as pd

def process_display():
    extracted = []
    niw = 0
    mbr = 0
    with open('1.csv', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if "Apple Macbook" in row[0]:
                    mbr += 1
                    line_count += 1
                    extracted.append(["mac_gpu", "mac_scr"])
                    continue
                try:
                    extracted.append(
                        [re.split(r'\t+', row[0].rstrip('\t'))[3],
                         re.split(r'\t+', row[0].rstrip('\t'))[5]])
                except IndexError:
                    niw += 1
                    extracted.append(["mac_gpu", "mac_scr"])
                line_count += 1
    gpu_list = []
    type_gpu = []
    vram = []
    size = []
    relu = []
    for e in extracted:
        temp = []
        x, y, z, w = "", "", "", ""
        if "NVIDIA" in e[0] or "nVidia" in e[0] or "Nvidia" in e[0]:
            x = "1"
            gpu_info = e[0].split(" ")
            for _ in gpu_info:
                if "GB" in _:
                    temp.append(_)
        else:
            x = "0"
        temp.append("0")
        y = temp[0]

        flags = [False, False]
        for c in e[1]:

            if c == " " or c == "-": flags[0] = True

            if not flags[0]:
                z += c

            if c == ")": flags[1] = False

            if flags[1]: w += c

            if c == "(": flags[1] = True

        if w == "":
            w = "1920x1080"

        if z == "mac_scr":
            z = "13.3"
            w = "2560x1600"
        y = re.sub("GB", "", y)
        z = re.sub('"', '', z)
        z = re.sub("inch", "", z)

        w = re.sub(r'\s+', ' ', w.lower())
        w = w.replace("*", "x")
        w = re.sub(" x ", "x", w)
        w = re.sub(" x", "x", w)
        w = re.sub("x ", "x", w)
        w = re.sub("16:9", "", w)
        type_gpu.append(x)
        vram.append(y)
        size.append(z)
        try:
            relu.append(w.split('cm')[-1])
        except:
            relu.append(w.lower())
    print(vram)
    df = pd.DataFrame({'Size': size, "Relu": relu, "Type GPU": type_gpu, 'VRAM': vram})
    df.to_csv('display.csv', encoding='utf8', sep='\t', index=False)