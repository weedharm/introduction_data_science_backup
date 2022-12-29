from  display import *


def no_accent_vietnamese(s):
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[ÍÌỈĨỊ]', 'I', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
    s = re.sub('đ', 'd', s)
    s = re.sub('Đ', 'D', s)
    return s


def process_name(text):
    data = text.split(" ")
    result = ''
    for d in data:
        if d == no_accent_vietnamese(d):
            result += d + ' '
    return result


def process_cpu(CPU):
    remove = ['INTEL CORE ', 'PROCESSOR ', 'AMD ', 'XEON ', 'INTEL CELERON PROCESSOR ', 'APPLE ', 'INTEL CELERON ',
              'INTEL PENTIUM SILVER ', 'INTEL ', 'PENTIUM ', 'PEN ', 'INTELCORE ']
    repl = ['RYZEN ', 'RYZEN', 'AMDR', 'RR']
    result = []
    for cpu in CPU:
        cpu = re.sub(r"[^a-zA-Z0-9\s]", "", cpu.split("(")[0].upper().replace("-", " ")).strip()
        cpu = re.sub("INTEL CORE 5", "INTEL CORE I5", cpu)
        cpu = re.sub("W ", "W", cpu)
        for ele in remove:
            cpu = re.sub(ele, "", cpu)
        for ele in repl:
            cpu = re.sub(ele, "R", cpu)
        cpu = re.sub("COREI", "I", cpu.strip())
        result.append(cpu.split(" ")[0])
    return result


def process_ram(RAM):
    total_ram = []
    for ram in RAM:
        ram = ram.split("GB")[0].strip().replace('*', ' x ').replace("G", "")
        try:
            ram = ram.replace("G(", "")
        except:
            pass
        if ' x ' in ram:
            temp = ram.split(' x ')
            total_ram.append(int(temp[0]) * int(temp[1]))
        else:
            total_ram.append(int(ram))
    return total_ram


def process_disk(DISK):
    type_disk = []
    capacity_disk = []
    for disk in DISK:
        temp_disk = str(disk).upper()
        temp_disk = re.sub("M.2 ", "", temp_disk)
        if 'SSD' in str(disk) or 'NVMe' in str(disk):
            type_disk.append(1)
        else:
            type_disk.append(0)
        try:
            capacity_disk.append(int(temp_disk.strip().split('GB')[0]))
        except:
            capacity_disk.append(int(temp_disk.strip().split('TB')[0]) * 1024)
    return type_disk, capacity_disk


def process_prices(Old_Price, New_Price):
    res = []
    for i in range(0, len(Old_Price)):
        try:
            old = int(Old_Price[i])
        except:
            old = 0
        try:
            new = int(New_Price[i])
        except:
            new = 0
        if old != 0 and new != 0:
            res.append(int((old + new) / 2))
        else:
            res.append((old + new))
    return res


def convert_disk(type_disk, capacity_disk):
    SSD = []
    HDD = []
    for i in range(0, len(type_disk)):
        if type_disk[i] == 1:
            SSD.append(capacity_disk[i])
            HDD.append(0)
        else:
            HDD.append(capacity_disk[i])
            SSD.append(0)
    return SSD, HDD


if __name__ == '__main__':
    process_display()
    data_display = pd.read_csv('display.csv', encoding='utf8', sep='\t')
    size_dis = [x for x in data_display['Size']]
    relu_dis = [x for x in data_display['Relu']]
    type_gpu = [x for x in data_display["Type GPU"]]
    vram = [x for x in data_display['VRAM']]
    log_relu = []
    for x in relu_dis:
        if ' ' in x:
            log_relu.append(x)
        if 'mm' in x or 'hz' in x or 'wva' in x or 'x' not in x:
            log_relu.append(x)
    print(log_relu)
    log_vram = []
    for r in vram:
        try:
            temp = float(r)
        except:
            log_vram.append(r)
    print(log_vram)

    data = pd.read_csv('1.csv', encoding='utf8', sep='\t')

    Name = [x.lower() for x in data['Name']]
    CPU = [x for x in data['CPU']]
    RAM = [x for x in data['RAM']]
    DISK = [x for x in data['DISK']]
    GPU = [x for x in data['GPU']]
    DISPLAY = [x for x in data['DISPLAY']]
    Old_Price = [x for x in data['Old Price']]
    New_Price = [x for x in data['New Price']]
    hz = []
    for scr in DISPLAY:
        if 'hz' not in scr.lower():
            hz.append(60)
        else:
            try:
                temp = scr.split(" ")
                for t in temp:
                    if 'hz' in t.lower():
                        hezt = re.sub('hz', '', t.lower())
                        hezt = re.sub(',', '', hezt)
                        hz.append(int(hezt))
                        break
            except:
                hz.append(60)
    print(hz)
    producer = [process_name(x).split(" ")[1] for x in Name]
    total_price = process_prices(Old_Price, New_Price)
    type_disk, capacity_disk = process_disk(DISK)
    total_ram = process_ram(RAM)
    totol_cpu = process_cpu(CPU)

    df = pd.DataFrame({'Name': Name, 'Producer': producer, 'CPU': totol_cpu, 'Ram': total_ram, 'Type disk': type_disk,
                       'Capacity': capacity_disk, 'Type GPU': type_gpu, 'VRAM': vram, "Size Display": size_dis, "HZ" : hz,
                       "Relu Display": relu_dis, 'Price': total_price})
    df = df.loc[df["Price"] != 0]
    for log in log_relu:
        df = df.loc[df["Relu Display"] != log]
    for log in log_vram:
        df = df.loc[df["VRAM"] != log]
    df = df.loc[df["Size Display"] != "Nvidia"]
    df.to_csv('final_data.csv', encoding='utf8', sep='\t', index=False)
