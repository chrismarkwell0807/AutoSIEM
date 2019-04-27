import wx
from gui import *
import gui
import sqlite3
import os
import string
# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details


db_file = "database.db"
try:
    os.remove(db_file)
except:
    print("No DB present!")

class ApplicationWindow(gui.mainWindow):
    def __init__(self, parent):
        gui.mainWindow.__init__(self,parent)

    def createDatabase(self, log):
        global db_file
        alphabet = ""
        alphabet = list(string.ascii_lowercase)
        print(alphabet)
        conn = sqlite3.connect(db_file)
        sql = conn.cursor()
        try:
            sql.execute('''CREATE TABLE logdatabase(timestamps, sID, category, classification, priority, protocol, srcIP, srcPort, dstIP, dstPort, importance)''')
        except:
            print("Database Already Exists")

        f = open(log)

        # read all the lines in the file and return them in a list
        logList = f.readlines()
        loglength = len(logList)
        # ensures number of rows in grid matches rows in the log file
        self.m_gridList.AppendRows(numRows=loglength, updateLabels=True)


        placeinlist = 0

        for line in logList:
            timestamps = line[0:14]
            timestamps = str(timestamps)# takes first 14 characters as time without milliseconds (DONE)
            self.m_gridList.SetCellValue(placeinlist, 0, timestamps)
            #print(timestamps)
            # populate timestamp column

            sID = line[28:len(line)]  # takes everything after time
            sID = sID.split()  # splits everything by whitespace into a list
            sID = sID[0]  # takes the first string in that list
            # print("unformatted " + sID)
            sID = sID[1: len(sID) - 1]  # seperates the sID from the brackets encasing it (DONE)
            sID = str(sID)
            # populate sID column
            self.m_gridList.SetCellValue(placeinlist, 1, sID)
            #print(sID)

            category = line.split("]")
            category = category[2]
            category = category[1:len(category) - 4]
            # populate category column
            self.m_gridList.SetCellValue(placeinlist, 2, category)
            # print(category)

            classification = line.split(":")  # splits line into list with ":" delimiter.
            classification = classification[5]  # takes 5th element from the split line.
            classification = classification[:-11]  # removes last 11 characters from the string -  ] [ Priority (DONE)
            # populate classification collumn
            self.m_gridList.SetCellValue(placeinlist, 3, classification)
            # print(classification)

            priority = line.split(":")  # splits up line into list with : delimiter.
            priority = priority[6]  # takes 6th element in list.
            priority = priority.strip()  # strips whitespace
            priority = priority[0]  # Grabs priority value
            self.m_gridList.SetCellValue(placeinlist, 4, priority)
            # print("priority: " + priority)

            protocol = line.split('{')  # splits using { delimiter.
            protocol = str(protocol[1]).split('}')  # converts to string, then split the first element into a list using the } delimiter
            protocol = protocol[0]  # takes first element in list as final protocol varable. (DONE)
            self.m_gridList.SetCellValue(placeinlist, 5, protocol)

            srcIP = line.split("}")  # splits with }
            srcIP = str(srcIP[1]).split()  # takes 1st element, splits by whitespace
            srcIP = srcIP[0]  # takes 0 element and assigns variable.

            try:
                if srcIP.count(":") == 1:
                    # this is an IPv4 address with a port!
                    SrcIsIPv6 = False
                    srcIP = srcIP.split(":")
                    srcPort = str(srcIP[1])
                    srcIP = str(srcIP[0])
                    # print(srcPort, srcIP)
                elif srcIP.count(":") == 0:
                    srcPort = ""
                    SrcIsIPv6 = False
                    # this is a IPv4 address without a port!
                elif srcIP.count(":") >= 2:
                    # this is an IPv6 address:
                    SrcIsIPv6 = True
                    srcIP = srcIP.split(":")
                    srcPort = srcIP[len(srcIP) - 1]
                    # checking for letters
                    for character in srcPort:
                        if character in alphabet:
                            isaport = False
                            srcPort = ""
                            break
                        else:  #
                            srcIP.remove(srcPort)
                            isaport = True
                            break
            except:
                print("except met!")
                srcPort = ""

            srcIP2 = ""
            if SrcIsIPv6 == True:
                for bit in srcIP:
                    srcIP2 = srcIP2 + bit + ":"
                srcIP = srcIP2[0:len(srcIP2) - 1]

            # --------------------   DESTINATION IP ------------------------------- #
            dstIP = line.split(">")  # splits with the > symbol.
            dstIP = dstIP[1].split()
            dstIP = dstIP[0]  # destination IP (DONE)


            try:
                if dstIP.count(":") == 1:
                    # this is an IPv4 address with a port!
                    DstIsIPv6 = False
                    dstIP = dstIP.split(":")
                    dstPort = str(dstIP[1])
                    dstIP = str(dstIP[0])
                    # print(dstPort, dstIP)
                elif dstIP.count(":") == 0:
                    dstPort = ""
                    DstIsIPv6 = False
                    # this is a IPv4 address without a port!
                elif dstIP.count(":") >= 2:
                    # this is an IPv6 address:
                    DstIsIPv6 = True
                    dstIP = dstIP.split(":")
                    dstPort = dstIP[len(dstIP) - 1]
                    # checking for letters
                    for character in dstPort:
                        if character in alphabet:
                            isaport = False

                            dstPort = ""
                            break
                        else:  #

                            dstIP.remove(dstPort)
                            isaport = True
                            break
            except:
                print("except met!")
                dstPort = ""
                DstIsIPv6 = False

            dstIP2 = ""
            if DstIsIPv6 == True:
                for bit in dstIP:
                    dstIP2 = dstIP2 + bit + ":"
                dstIP = dstIP2[0:len(dstIP2) - 1]


            srcIP = str(srcIP)
            dstIP = str(dstIP)
            self.m_gridList.SetCellValue(placeinlist, 6, srcIP)
            self.m_gridList.SetCellValue(placeinlist, 7, srcPort)
            self.m_gridList.SetCellValue(placeinlist, 8, dstIP)
            self.m_gridList.SetCellValue(placeinlist, 9, dstPort)

            importance = 0
            badports = ['20', '21', '22', '23', '8080', '137', '138', '139' , '161', '162']
            verybadports = ['80', '443']
            badwords = ["ATTACK","LEAK", "EXPLOIT", "VIOLATION",  "SCAN", "VULNERABLE", "EXECUTABLE", "METASPLOIT", "TROJAN", "VIRUS", "COMMAND", "INJECTION", "SCRIPTING", "TRAVERSAL"]
            goodwords = ["POTENTIAL", "MISC","PING"]
            classificationwordlist = classification.split()
            categorywordlist = category.split()

            if priority == '2':
               importance += 1
            elif priority == '1':
               importance += 2

            for port in range(0, len(badports)):
                if srcPort == badports[port]:
                    importance += 1
                elif dstPort == badports[port]:
                    importance += 1


            for port in range(0, len(verybadports)):
                if srcPort == verybadports[port]:
                    importance += 3
                elif dstPort == verybadports[port]:
                    importance += 3



            for word in classificationwordlist:
                if word.upper() in badwords:
                    importance += 1
                elif word.upper() in goodwords:
                    importance -= 1
                    # print("goodword met")

            for word in categorywordlist:
                if word.upper() in badwords:
                    importance += 1
                elif word.upper() in goodwords:
                    importance -= 1


            # if statement to check for decrease importance ( potential / misc" in classification etc

            self.m_gridList.SetCellValue(placeinlist, 10, str(importance))

            row = []
            row.append(timestamps)
            row.append(sID)
            row.append(category)
            row.append(classification)
            row.append(priority)
            row.append(protocol)
            row.append(srcIP)
            row.append(srcPort)
            row.append(dstIP)
            row.append(dstPort)
            row.append(importance)

            sql.execute('INSERT INTO logdatabase VALUES (?,?,?,?,?,?,?,?,?,?,?);', (row))
            sortby = 'timestamps'

            placeinlist += 1
        conn.commit()
        conn.close()


    #   ******    Nathans method of updating grid column based on db column.
    # placeinlist = 0
    # for rowdata in sql.execute('SELECT sID FROM table ORDER BY timestamps'):
    #     self.grid.SetCellValue(placeinlist, timestamps - column, rowdata)
    # placeinlist += 1


    def readLog(self, event):
        file = self.m_filePicker.GetPath()

        self.createDatabase(file)
        self.m_textCtrl.SetValue("Done!") # debug for button working.


    def SortAscend( self, event ):
        def sort(self, sortValue):

            global db_file
            conn = sqlite3.connect(db_file)
            sql = conn.cursor()

            placeinlist = 0
            sqlCommand = "SELECT timestamps FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 0, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT sID FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 1, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT category FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 2, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT classification FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 3, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT priority FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 4, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT protocol FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 5, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT srcIP FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 6, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT srcPort FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 7, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT dstIP FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 8, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT dstPort FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 9, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT importance FROM logdatabase ORDER BY " + sortValue + " ASC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 10, str(row[0]))
                placeinlist += 1


            conn.commit()
            conn.close()
        if self.m_comboBoxSort.GetValue() == "Timestamps":
            sortValue = 'timestamps'
        elif self.m_comboBoxSort.GetValue() == "sID":
            sortValue = 'sID'
        elif self.m_comboBoxSort.GetValue() == "Category":
            sortValue = 'category'
        elif self.m_comboBoxSort.GetValue() == "Classification":
            sortValue = 'classification'
        elif self.m_comboBoxSort.GetValue() == "Priority":
            sortValue = 'priority'
        elif self.m_comboBoxSort.GetValue() == "Protocol":
            sortValue = 'protocol'
        elif self.m_comboBoxSort.GetValue() == "Source IP":
            sortValue = 'srcIP'
        elif self.m_comboBoxSort.GetValue() == "Destination IP":
            sortValue = 'dstIP'
        elif self.m_comboBoxSort.GetValue() == "Source Port":
            sortValue = 'srcPort'
        elif self.m_comboBoxSort.GetValue() == "Destination Port":
            sortValue = 'dstPort'
        elif self.m_comboBoxSort.GetValue() == "Importance":
            sortValue = 'importance'


        sort(self, sortValue)


    def SortDescend( self, event ):
        def sort(self, sortValue):

            global db_file
            conn = sqlite3.connect(db_file)
            sql = conn.cursor()

            placeinlist = 0
            sqlCommand = "SELECT timestamps FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 0, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT sID FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 1, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT category FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 2, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT classification FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 3, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT priority FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 4, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT protocol FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 5, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT srcIP FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 6, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT srcPort FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 7, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT dstIP FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 8, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT dstPort FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 9, row[0])
                placeinlist += 1

            placeinlist = 0
            sqlCommand = "SELECT importance FROM logdatabase ORDER BY " + sortValue + " DESC"
            for row in sql.execute(sqlCommand):
                self.m_gridList.SetCellValue(placeinlist, 10, str(row[0]))
                placeinlist += 1

            conn.commit()
            conn.close()
        if self.m_comboBoxSort.GetValue() == "Timestamps":
            sortValue = 'timestamps'
        elif self.m_comboBoxSort.GetValue() == "sID":
            sortValue = 'sID'
        elif self.m_comboBoxSort.GetValue() == "Category":
            sortValue = 'category'
        elif self.m_comboBoxSort.GetValue() == "Classification":
            sortValue = 'classification'
        elif self.m_comboBoxSort.GetValue() == "Priority":
            sortValue = 'priority'
        elif self.m_comboBoxSort.GetValue() == "Protocol":
            sortValue = 'protocol'
        elif self.m_comboBoxSort.GetValue() == "Source IP":
            sortValue = 'srcIP'
        elif self.m_comboBoxSort.GetValue() == "Destination IP":
            sortValue = 'dstIP'
        elif self.m_comboBoxSort.GetValue() == "Source Port":
            sortValue = 'srcPort'
        elif self.m_comboBoxSort.GetValue() == "Destination Port":
            sortValue = 'dstPort'
        elif self.m_comboBoxSort.GetValue() == "Importance":
            sortValue = 'importance'


        sort(self, sortValue)




print("Starting App...")
app = wx.App(False)
frame = ApplicationWindow(None)

frame.Show(True)
app.MainLoop()

