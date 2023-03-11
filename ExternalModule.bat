
#definition of the bat file as as string
#it will be equivalent to manually type these commands line by line
batF="""@echo off
    call "->QGISPATH<-\\o4w_env.bat"
    call "py3_env"
    call python -m pip install -r \"->HOMEPATH<-requirements.txt\"
    call exit
    @echo on
    """

# then the idea is to find the osgeo4w shell path
# sys.executable is the base execution path and contains o4w_env.bat
# o4w_env.bat setup the osgeo4w shell
qgispath = str(os.path.dirname(sys.executable))

# here you replace the string ->QGISPATH<- with qgis path
# so that the script is installation independant
batF = batF.replace("->QGISPATH<-",qgispath)

# and the string ->HOMEPATH<- with the path to your requirements.txt
req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
batF = batF.replace("->HOMEPATH<-", req_file)


