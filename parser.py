import time
start_time = time.time()

titles = []
ddls = []

try:
    with open("target.txt", "r", encoding="UTF-8") as f:
        packages = f.readlines()
        pkgs = []
        for pkg in packages:
            try:
                for _ in range(5):
                    try:
                        title = pkg.split("http")[0].split(["Minis", "PSP", "NeoGeo", "Go", "PC Engine"][_])[1]
                        break
                    except: pass
                try:
                    title = title.strip() 
                except NameError:
                    continue
                titles.append(title)
                package = ("http" + pkg.split("http")[1]).split(".pkg")[0] + ".pkg"
                ddls.append(package)
                print("Parsed Game: %s \nDDL: %s" % (title, package))
            except IndexError:
                print("Passed Exception IndexError (could not find DDL)")
except FileNotFoundError:
    print("target.txt not found! Insert your PKGI games file named to 'target.txt'")

with open("titles.txt", "w", encoding="UTF-8") as titledata:
    for title in titles:
        titledata.write("%s\n" % str(title))
with open("ddls.txt", "w", encoding="UTF-8") as downloaddata:
    for ddl in ddls:
        downloaddata.write("%s\n" % str(ddl))

end_time = time.time()
print("\nJob Finished! (%sms)" % str(round((end_time - start_time) * 1000)))