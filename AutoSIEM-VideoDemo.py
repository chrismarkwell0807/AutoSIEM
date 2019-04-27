import wx
from gui import *
import gui
import sqlite3

# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details


db_file = "database.db"

class ApplicationWindow(gui.mainWindow):
    def __init__(self, parent):
        gui.mainWindow.__init__(self,parent)

    def createDatabase(self, log):
        global db_file

        conn = sqlite3.connect(db_file)
        sql = conn.cursor()
        try:
            sql.execute('''CREATE TABLE logdatabase(time, sID, category, classification, priority, protocol, srcIP, dstIP)''')
        except:
            print("Database Already Exists")

        f = open(log)

        # read all the lines in the file and return them in a list
        logList = f.readlines()
        loglength = len(logList)
        #ensures number of rows in grid matches rows in the log file
        self.m_gridList.AppendRows(numRows=loglength, updateLabels=True)


        placeinlist = 0

        for line in logList:
            timestamps = line[0:14]
            timestamps = str(timestamps)# takes first 14 characters as time without milliseconds (DONE)
            #print(timestamps)
            self.m_gridList.SetCellValue(placeinlist, 0, timestamps)
            # populate timestamp column

            sID = line[28:len(line)]  # takes everything after time
            sID = sID.split()  # splits everything by whitespace into a list
            sID = sID[0]  # takes the first string in that list
            # print("unformatted " + sID)
            sID = sID[1: len(sID) - 1]  # seperates the sID from the brackets encasing it (DONE)
            sID = str(sID)
            self.m_gridList.SetCellValue(placeinlist, 1, sID)
            # populate sID column
            #print(sID)

            category = line.split("]")
            category = category[2]
            category = category[1:len(category) - 4]
            self.m_gridList.SetCellValue(placeinlist, 2, category)
            # populate category column
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
            self.m_gridList.SetCellValue(placeinlist, 6, srcIP)

            #print("src: " + srcIP)

            dstIP = line.split(">")  # splits with the > symbol.
            dstIP = dstIP[1].split()
            dstIP = dstIP[0]  # destination IP (DONE)
            self.m_gridList.SetCellValue(placeinlist, 7, dstIP)

            # print(dstIP)
            row = []
            row.append(timestamps)
            row.append(sID)
            row.append(category)
            row.append(classification)
            row.append(priority)
            row.append(protocol)
            row.append(srcIP)
            row.append(dstIP)
            sql.execute('INSERT INTO logdatabase VALUES (?,?,?,?,?,?,?,?);', (row))
            sortby = 'timestamps'
            # print("Row added to db")
            placeinlist += 1
        conn.commit()
        conn.close()
        updateGrid(sortby)

    #   ******    Nathans method of updating grid column based on db column.
    # placeinlist = 0
    # for rowdata in sql.execute('SELECT sID FROM table ORDER BY timestamps'):
    #     self.grid.SetCellValue(placeinlist, timestamps - column, rowdata)
    # placeinlist += 1


    def readLog(self, event):
        file = self.m_filePicker.GetPath()
        print("DEBUG | Selected file: " + file) # - file that is picked.
        self.createDatabase(file)
        self.m_textCtrl.SetValue("Done!") # debug for button working.


    # def updateGrid(self, sortby):
    #
    #
    #     global db_file
    #     conn = sqlite3.connect(db_file)
    #     sql = conn.cursor()






        print("sorting by")
        for i in sortby:
            print(str(i))

    def openSortWindowDialog(self, event):
        SortByWindow = SortByWindowDialog(self, ApplicationWindow)
        SortByWindow.Show()




class SortByWindowDialog(gui.SortByWindow):

    def __init__(self, parent, ApplicationWindow):
        gui.SortByWindow.__init__(self, parent)




print("Starting App...")
app = wx.App(False)
frame = ApplicationWindow(None)

frame.Show(True)
app.MainLoop()

