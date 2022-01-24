from os import environ as env
from os import scandir
import datetime as dt
import pysftp

def return_most_recent(pattern, lst):
    """Takes a pattern and a list from ftp.retrlines output (not ordered).
    Returns the filename which matches the pattern and is most recent by
    date and timestamp."""
    
    matches = []
    fmt = "%b %d %Y %H:%M"
    #now = dt.datetime.now()
    #yr = str(now.year) #this doesn't work past new year, see yr in loop below
    fixed_times = []
    for line in lst:
        if pattern in line:
            matches.append(line)
    for match in matches:
        l = match.split()
        #get the year from the title because you can't from the filewrite timestamp
        filename_slug = l[-1].split("_") #returns list, i=4,5 are dates pulled from name
        date_component = dt.datetime.strptime(filename_slug[5], "%Y%m%d") #use year from end date span
        yr = str(date_component.year)
        l.insert(7, yr)
        stamp = dt.datetime.strptime(" ".join(l[5:9]), fmt)
        fixed_times.append((stamp, l[-1]))
    lowest = [ y for x, y in fixed_times if x == max([ x for x, y in fixed_times]) ]
    return lowest[0]

def print_dir(dir):
    dir_list = []
    with scandir(dir) as dir:
        for f in dir:
            dir_list.append((f.name, dt.datetime.fromtimestamp(f.stat()[8])))
    for (file, time) in sorted(dir_list):
        print("{} : {}".format(file, time))
    

if __name__ == "__main__":
    url = env.get("FTPURL")
    user = env.get("FTPUSER")
    pw = env.get("FTPPW")
    port = env.get("FTPPORT")
    
    options = pysftp.CnOpts()
    options.hostkeys = None
    with pysftp.Connection(url, username=user, password=pw, port=int(port), cnopts=options) as sftp:
        dir_objs = sftp.listdir_attr()
        lst_items = [ line.longname for line in dir_objs ]
        filename = return_most_recent("REPORT_UBD.csv", lst_items)
        sftp.get(filename, localpath=f"archives/{filename}", preserve_mtime=True)
    print(f"Downloaded {filename} and placed it in archives")
    print_dir("archives")