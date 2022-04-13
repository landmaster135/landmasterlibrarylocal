# Library by default
from pathlib import Path
import sys
# Library by third party
import yaml
# Library in the local


def getStrRepeatedToMark(repeatStr : str, repeatNumberToMark : int = 15) -> str:
    return str(repeatStr * repeatNumberToMark)

def outputLog(className : str, functionName : str, remark : str) -> None:
    print("{className}: {functionName}: {remark}".format(
        className=className,
        functionName=functionName,
        remark=remark
    ))

def getStrFromList(targetList : list) -> str:
    separator = ","
    bracketStart = "["
    bracketEnd   = "]"
    resultStr = ""
    for i in targetList:
        if resultStr == "":
            resultStr = "{}{}".format(resultStr, str(i))
        else:
            resultStr = "{}{}{}".format(resultStr, separator, str(i))
    resultStr = "{} {} {}".format(bracketStart, resultStr, bracketEnd)
    return resultStr

def getObjFromYaml(yamlFile):
    # className = self.__class__.__name__
    # functionName = sys._getframe().f_code.co_name
    with open(yamlFile) as file:
        obj = yaml.safe_load(file)
    return obj

def getValueFromYaml(yamlFile, field):
    className = __name__
    functionName = sys._getframe().f_code.co_name
    value = ""
    obj = getObjFromYaml(yamlFile)
    try:
        value = obj[field]
    except KeyError:
        raise ValueError("{className}: {functionName}: {message}".format(
            className=className,
            functionName=functionName,
            message=obj["msgObj_E0102"]
        ))
    return value

def getSrcPathFromTestPath(srcFileName : str, srcFolderName : str = "src") -> str:
    degreeOfParentDirectory = 2 - 1
    srcPath = str(Path(__file__).parents[degreeOfParentDirectory] / srcFolderName / srcFileName)
    return srcPath
