import requests
import sys

def main():
    try:
        f = open(sys.argv[1],'r')
    except IndexError:
        print("[!] Usage: python3 BurpLog2py.py BurpLog OutPutFileName")
        exit(0)
    except IOError:
        print("[!] %", sys.exc_info())
        exit(0)

    url = ""
    method = ""
    params = {}
    headers = {}
    data = {}

    i = 0
    lines = f.readlines()
    for line in lines:
        if i == 0:
            method = line.split()[0]
            if method == 'GET':
                try:
                    url = line.split()[1].split("?")[0]
                    for param in line.split()[1].split("?")[1].split("&"):
                        params[param.split("=")[0]] = param.split("=")[1]
                except IndexError:
                    pass
            else:
                url = line.split()[1]
            i += 1
            continue
        elif i == 1:
            url = "http://" + line.split(":")[1].strip() + url
            i += 1
            continue
        elif line == '\n':
            for postdatas in lines[i+1:]:
                for postdata in postdatas.split("&"):
                    try:
                        data[postdata.split("=")[0]] = postdata.split("=")[1]
                    except IndexError:
                        data[postdata.split("=")[0]] = 'Null'
            break
        else:
            headers[line.split(":",1)[0]] = line.split(":",1)[1].strip()
            i += 1


    f.close()

    try:
        f = open(sys.argv[2],'w')
    except IndexError:
        print("[!] Usage: python3 BurpLog2py.py BurpLog OutPutFileName\n")
        exit(0)
    f.write("import requests\n")
    f.write("\n")
    f.write("url = '" + url + "'\n")
    if params:
        f.write("params = {\n")
        for (key, value) in params.items():
            f.write("    '" + key + "' : '" + value + "',\n")
        f.write("}\n")
    if data:
        f.write("data = {\n")
        for (key, value) in data.items():
            f.write("    '" + key + "' : '" + value + "',\n")
        f.write("}\n")
    if headers:
        f.write("headers = {\n")
        try:
            for (key, value) in headers.items():
                f.write("    '" + key + "': '" + value + "',\n")
            f.write("}\n\n")
        except:
            pass

    if method == "GET":
        f.write("r = requests.get(url, params=params, headers=headers)\n")
    if method == "POST":
        f.write("r = requests.post(url, data=data,headers=headers)\n")
    f.write("print(r.status_code)\n")
    f.write("print(r.content)")

    f.close()

if __name__ == '__main__':
    main()

