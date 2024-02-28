import time, requests, re
from tqdm import tqdm
start_time = time.time()

ddls = open("ddls.txt", "r").readlines()
names = []

try:
    with open("titles.txt", "rb") as titles:
        for index, title in enumerate(titles.readlines()):
            if index > len(ddls):
                break
            print("%s. %s" % (index+1, title.decode("UTF-8", errors="ignore").strip()))
            names.append(title.decode("UTF-8", errors="ignore").strip())
except FileNotFoundError:
    print("titles.txt not found! Make sure to use parser.py before downloading.")

filereadable = lambda s: re.sub(r'[^\w\s]', '', s.strip().replace('[', '').replace(']', ''))[:255]


try:
    getDDL = int(input("\nGame Number: "))
    print("Downloading game:\nDDL: %s\nName: %s\nFile Name: %s" % (ddls[getDDL-1].strip(), names[getDDL-1], filereadable(names[getDDL-1]) + ".pkg"))

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

end_time = time.time()
print("\nJob Finished! (%sms)" % str(round((end_time - start_time) * 1000)))
