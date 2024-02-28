import time, requests
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

try:
    getDDL = int(input("\nGame Number: "))
    print("Downloading game:\nDDL: %s\nName: %s" % (ddls[getDDL-1].strip(), names[getDDL-1]))
    content = requests.get(ddls[getDDL-1].strip()).content
    print("Got game file, writing file...")
    pkg = (ddls[getDDL-1].strip())[::-1][:20][::-1]

    open(pkg, "wb").write(content)
    print("File Written! (%s)" % pkg)
except ValueError:
    print("ValueError - Incorrect Number")
except IndexError:
    print("Incorrect number value")

end_time = time.time()
print("\nJob Finished! (%sms)" % str(round((end_time - start_time) * 1000)))