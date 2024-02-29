import time, requests, re, os
from tqdm import tqdm
import random, string
start_time = time.time()

ddls = []
names = []

tmp = random.SystemRandom().choices(string.ascii_letters, k=25)

db = int(input("""
1. PSP Games (most stable)
2. PSP DLCs
3. PSP Themes
4. PSP Updates
Choice: """))

database = [
    "https://nopaystation.com/tsv/PSP_GAMES.tsv",
    "https://nopaystation.com/tsv/PSP_DLCS.tsv",
    "https://nopaystation.com/tsv/PSP_THEMES.tsv",
    "https://nopaystation.com/tsv/PSP_UPDATES.tsv"
][db-1]

kwargs = [
    [0,1,2,3,4,6,9],
    [0,1, "DLC", 2, 3, 5, 8],
    [0,1, "THEME", 2, 3, 5, 8],
    [0, 1, "UPDATE", 2, 3,5, 8]
][db-1]


f = open("".join(tmp), "wb")
f.write(requests.get(database).content)
f.close()

_database = open("QuickPKG_database.txt", "w", encoding="UTF-8")

with open("".join(tmp), "r", encoding="UTF-8", errors="ignore") as pkgs:
    for e, pkg in enumerate(pkgs.readlines()):
        if e == 0:
            continue
        package = pkg.encode()
        data = package.decode().split("\t")
        r_code = data[kwargs[0]]
        region = data[kwargs[1]]
        try:
            _type = data[kwargs[2]]
        except TypeError: _type = kwargs[2]
        title = data[kwargs[3]]
        ddl = data[kwargs[4]]
        date = data[kwargs[5]]
        try:
            size = int(data[kwargs[6]])
        except ValueError:
            size = 0
        msg = """
Package #%s:
Region Code: %s
Region: %s
Type: %s
Title: %s
DDL: %s
Date Modified: %s
File size: %smb
        """ % (e, r_code, region, _type, title, ddl, date, round(size/1048576, 2))
        _database.write(msg)
        print(msg)
        ddls.append(ddl)
        names.append(title)

print("Note: this database has been saved to QuickPKG_database.txt")
pkgs.close()
_database.close()

filereadable = lambda s: re.sub(r'[^\w\s]', '', s.strip().replace('[', '').replace(']', ''))[:255]
try:
    getDDL = int(input("\nItem Number: "))
    print("Downloading Item:\nDDL: %s\nName: %s\nFile Name: %s" % (ddls[getDDL-1].strip(), names[getDDL-1], filereadable(names[getDDL-1]) + ".pkg"))

    url = ddls[getDDL-1].strip()
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filereadable(names[getDDL-1]) + ".pkg", 'wb') as file, tqdm(
        desc="Downloading",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress_bar.update(len(data))

except ValueError:
    print("ValueError - Incorrect Number")
except IndexError:
    print("Incorrect number value")

os.remove("".join(tmp))

end_time = time.time()
print("\nJob Finished! (%sms)" % str(round((end_time - start_time) * 1000)))
