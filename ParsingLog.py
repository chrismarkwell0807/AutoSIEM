# the open keyword opens a file in read-only mode by default
import sqlite3

f = open("C:\\Users\\Chris\\PycharmProjects\\django\\TKDiss\\Logs\\maccdc2012_fast_alert\\alert.fast.maccdc2012_00000.pcap")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# read all the lines in the file and return them in a list
logList = f.readlines()

db_file = "database2.db"

conn = sqlite3.connect(db_file)
sql = conn.cursor()
try:
    sql.execute('''CREATE TABLE logdatabase(time, sID, category, classification, priority, protocol, srcIP, srcPort, dstIP, dstPort)''')
except:
    print("Database Already Exists")
for line in logList:
    timestamps = line[0:14] #takes first 14 characters as time without milliseconds (DONE)
    # print(time)

    sID = line[28:len(line)] #takes everything after time
    sID = sID.split() #splits everything by whitespace into a list
    sID = sID[0]#takes the first string in that list
    # print("unformatted " + sID)
    sID = sID[1: len(sID)-1] #seperates the sID from the brackets encasing it (DONE)
    # print(sID)

    category = line.split("]")
    category = category[2]
    category = category[1:len(category)- 4]
    # print(category)

    classification = line.split(":") # splits line into list with ":" delimiter.
    classification = classification[5] # takes 5th element from the split line.
    classification = classification[:-11] # removes last 11 characters from the string -  ] [ Priority (DONE)
    # print(classification)

    priority = line.split(":") # splits up line into list with : delimiter.
    priority = priority[6] # takes 6th element in list.
    priority = priority.strip() # strips whitespace
    priority = priority[0] # Grabs priority value
    # print("priority: " + priority)

    protocol = line.split('{') # splits using { delimiter.
    protocol = str(protocol[1]).split('}') # converts to string, then split the first element into a list using the } delimiter
    protocol = protocol[0] # takes first element in list as final protocol varable. (DONE)
    # print(protocol)

    srcIP = line.split("}") # splits with }
    srcIP = str(srcIP[1]).split() # takes 1st element, splits by whitespace
    srcIP = srcIP[0] # takes 0 element and assigns variable.
    # print("src: " + srcIP)

    try:
        if srcIP.count(":") == 1:
            # this is an IPv4 address with a port!
            srcIP = srcIP.split(":")
            srcPort = str(srcIP[1])
            srcIP = str(srcIP[0])
            # print(srcPort, srcIP)
        elif srcIP.count(":") == 0:
            srcPort = ""
            # this is a IPv4 address without a port!
        elif srcIP.count(":") >= 2:
            # this is an IPv6 address:
            srcIP = srcIP.split(":")
            srcPort = srcIP[len(srcIP) - 1]
            # checking for letters
            for character in srcPort:
                if character in alphabet:
                    isaport = False
                    srcPort = ""
                    break
    except:
        srcPort = ""




    dstIP = line.split(">") # splits with the > symbol.
    dstIP = dstIP[1].split()
    dstIP = dstIP[0]# destination IP (DONE)
    # print(dstIP)

    try:
        if dstIP.count(":") == 1:
            # this is an IPv4 address with a port!
            dstIP = dstIP.split(":")
            dstPort = str(dstIP[1])
            dstIP = str(dstIP[0])
            # print(dstPort, dstIP)
        elif dstIP.count(":") == 0:
            dstPort = ""
            # this is a IPv4 address without a port!
        elif dstIP.count(":") >= 2:
            # this is an IPv6 address:
            dstIP = dstIP.split(":")
            dstPort = dstIP[len(dstIP) - 1]
            # checking for letters
            for character in dstPort:
                if character in alphabet:
                    isaport = False
                    dstPort = ""
                    break
    except:
        dstPort = ""

    sql.execute('INSERT INTO logdatabase VALUES (?,?,?,?,?,?,?,?,?,?);',(timestamps, sID, category, classification, priority, protocol, srcIP, srcPort ,dstIP, dstPort))
conn.commit()
conn.close()
    

"""
print(lines[0][0:14])#example of time
print(lines[0].split["*"])
f.close()
"""
