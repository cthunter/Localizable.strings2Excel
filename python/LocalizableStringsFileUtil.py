#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,shutil
from Log import Log
import codecs
from fuzzywuzzy import process

class LocalizableStringsFileUtil:
    'iOS Localizable.strings file util'

    @staticmethod
    def writeToFile(keys,values,directory,additional):
        if not os.path.exists(directory):
            os.makedirs(directory)

        Log.info("Creating iOS file:" + directory+"Localizable.strings")

        fo = open(directory+"Localizable.strings", "wb")

        for x in range(len(keys)):
            if values[x] is None or values[x] == '':
                Log.error("Key:" + keys[x] + "\'s value is None. Index:" + str(x + 1))
                continue

            key = keys[x]
            value = values[x]
            content = "\"" + key + "\" " + "= " + "\"" + value + "\";\n"
            fo.write(content);

        if additional is not None:
            fo.write(additional)

        fo.close()


    @staticmethod
    def getKeysAndValues(path):
        if path is None:
            Log.error('file path is None')
            return

        # 1.Read localizable.strings
        file = codecs.open(path, 'r', 'utf-8')
        string = file.read()
        file.close()

        # 2.Split by ";
        localStringList = string.split('\";')
        list = [x.split(' = ') for x in localStringList]

        # 3.Get keys & values
        keys = []
        values = []
        for x in range(len(list)):
            keyValue = list[x]
            if len(keyValue) > 1:
                key = keyValue[0].split('\"')[1]
                value = keyValue[1][1:]
                keys.append(key)
                values.append(value)

        return (keys,values)

    @staticmethod
    def fuzzyReplaceLocalizableFile(keys,values,directory,additional):
        if not os.path.exists(directory):
            return

        Log.info("Open iOS file:" + directory+"Localizable.strings")
        fn = directory+"Localizable.strings"
        shutil.copyfile(fn,fn+".bak")

        fo = open(directory+"KeyMap.txt", "wb")
        (okeys,ovalues) = LocalizableStringsFileUtil.getKeysAndValues(fn)
        

        for x in range(len(values)):
            if values[x] is None or values[x] == '':
                Log.error("Key:" + keys[x] + "\'s value is None. Index:" + str(x + 1))
                continue

            key = keys[x]
            value = values[x]

            (ovalue,ratio) = process.extractOne(value,ovalues)

            if ratio > 80 :
                oindex = ovalues.index(ovalue)
                Log.info("found a string '"+ovalue+"' with key '"+key+"' index: "+str(oindex))
                content = okeys[oindex] + ","+ key + "\n"
                fo.write(content);

        fo.close

        LocalizableStringsFileUtil.writeToFile(keys,values,directory,additional)        

            # content = "\"" + key + "\" " + "= " + "\"" + value + "\";\n"
            # fo.write(content);

        # if additional is not None:
        #     fo.write(additional)

        # fo.close()