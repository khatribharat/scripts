import os
import subprocess

def onWalkError(e):
    print("Directory walk error: " + str(e))

if __name__ == '__main__':
    deployDate1 = "10-March-2015"
    deployDate2 = "5-May-2015"
    dir = "/home/khatri/toolbar-war/" + deployDate1 + "/WEB-INF/"
    numFiles = 0
    numDiff = 0
    numErrors = 0
    for dirpath, dirnames, filenames in os.walk(dir, onerror=onWalkError):
        for filename in filenames:
            numFiles += 1
            filename1 = os.path.join(dirpath, filename)
            filename2 = os.path.join(dirpath.replace(deployDate1, deployDate2), filename)
            print("[" + str(numFiles) + "] Comparing " + filename1 + ", " + filename2)
            returnCode = subprocess.call(["cmp", "-b", filename1, filename2])
            if returnCode == 1:
                numDiff += 1
            elif returnCode == 2:
                numErrors += 1
    print("Number of different files : " + str(numDiff))
    print("Number of errors : " + str(numErrors))