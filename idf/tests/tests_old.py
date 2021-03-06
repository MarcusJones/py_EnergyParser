#===============================================================================
# Set up
#===============================================================================
# Standard:



from config import *

import logging.config
import unittest

from ExergyUtilities.utility_inspect import get_self
#from utility_pathOLD import split_up_path 
# Testing imports
#from ..IDF import IDF
import idf.idf_parser as idf
from idf.utilities_idf_xml import printXML
from UtilityLogger import loggerCritical

#get_table_all_names

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================
class IDDTests(unittest.TestCase):
    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        currentPath = split_up_path(__file__)
        projectRootPath = currentPath[:-4]
        sampleFileDir = ["SampleIDFs"]
        sampleFile1 = ["Energy+.iddSAMPLE"]  
        pathIDDsample1 = projectRootPath + sampleFileDir + sampleFile1
        self.pathIDDsample  = os.path.join(*pathIDDsample1)
        
        sampleFile2 = ["Energy+.idd"]  
        pathIDDsample2 = projectRootPath + sampleFileDir + sampleFile2
        self.pathIDDfull = os.path.join(*pathIDDsample2)
        
    def test010_IDDSample(self):
        print( "**** TEST {} ****".format(get_self()))
        testIDD = idf.idf_parse.from_IDD_file(self.pathIDDsample)
        printXML(testIDD.XML)
        
    def test020_IDD_FULL(self):
        print( "**** TEST {} ****".format(get_self()))

        testIDD = idf.idf_parse.from_IDD_file(self.pathIDDfull)

        testIDD.write_XML(r"c:\\temp\\test.xml")
        
        for item in idf.tree_get_class(testIDD.XML,"Vers",False):
            printXML(item)

class IDFtests(unittest.TestCase):
    
    def setUp(self):
        print( "**** TEST {} ****".format(get_self()))
        currentPath = split_up_path(__file__)

        thisProjRoot = split_up_path(os.getcwd())[:4] 
        thisTestExcelProj = "\\".join(thisProjRoot) + r"\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
        self.thisTestExcelProj = thisTestExcelProj
        #projectFile = r"C:\Eclipse\PyIDF\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
        projectRootPath = currentPath[:-4]
        sampleFileDir = ["SampleIDFs"]
        sampleFile1 = ["5ZoneFPIU.idf"]  
        sampleFile2 = ["r00 MainIDF.idf"]
        path_5Zone = projectRootPath + sampleFileDir + sampleFile1
        self.path_5Zone  = os.path.join(*path_5Zone)
        path_CentralTower = projectRootPath + sampleFileDir + sampleFile2
        self.path_CentralTower = os.path.join(*path_CentralTower)



        
    def test010_SimpleCreation(self):
        print( "**** TEST {} ****".format(get_self()))
        
        testIDF = idf.idf_parse.from_IDF_file(self.path_5Zone)
        #print testIDF
        #print listZones(testIDF)
        #countAllClasses(testIDF, printFlag = 1)
        
        objTable = idf.get_table_all_names(testIDF)
        #printStdTable(objTable)
        cntTable = idf.get_table_object_count(testIDF)
        print( testIDF.num_objects)
        newIDF = testIDF + testIDF

        #print testIDF.num_objects
        #print newIDF.num_objects
        #print testIDF.num_objects
        
        #assert(newIDF.num_objects == testIDF.num_objects)
        #printStdTable(cntTable)
        

    def test020_checkTemplates(self):
        print( "**** TEST {} ****".format(get_self()))

        templates = idf.loadTemplates(IDF_TEMPLATE_PATH)
        
        testIDF = idf.idf_parse.from_IDF_file(self.path_5Zone)
        with loggerCritical():
            for template in templates:
                testIDF = testIDF + template

        print( "{} templates passed addition test".format(len(templates)))

        #pp = pprint.PrettyPrinter(indent=4)
        #lastTemplate = templates.pop()
        #print lastTemplate
        #print pp.pprint(lastTemplate.templateDef)
        
    def test030_getVariants(self):
        #weatherFilePath = FREELANCE_DIR + r"\WEA\ARE_Abu.Dhabi.412170_IWEC.epw"
        #outputDirPath = FREELANCE_DIR + r"\Simulation"    
        #groupName = "00myGroup"
        #===========================================================================
        # Assemble!
        #===========================================================================
        #idfAssembly(projectFile,weatherFilePath,outputDirPath,groupName)
        variants = idf.load_cariants(self.thisTestExcelProj)
        
    def test040_cleanObjects(self):
        print( "**** TEST {} ****".format(get_self()))
        myIDF = idf.idf_parse.from_IDF_file(self.path_CentralTower)
        #printStdTable(get_table_object_count(myIDF))
        
        #zoneObjs = tree_get_class(myIDF.XML, "Zone")
        #print idfGetZoneNameList(myIDF)
        #printStdTable(get_table_object_count(myIDF))
        #print keptClassesDict['onlyGeometry']
        #print myIDF.num_objects
        idf.clean_out_object(myIDF, idf.keptClassesDict['onlyGeometry'])
        #print myIDF.num_objects
        assert(myIDF.num_objects == 224)
        #printStdTable(get_table_object_count(myIDF))


        
    def test050_applyTemplates(self):
        print( "**** TEST {} ****".format(get_self()))
        variants = idf.load_cariants(self.thisTestExcelProj)
        
        # Customize for test
        myVariant = next(iter(variants.values()))
        #pPrint(myVariant)
        myVariant["source"] = self.path_CentralTower
        myVariant["templates"] = [{'templateName': 'Generic lights', 'zones': '.'}]
        myVariants = [myVariant]
        
        #assemble_variants(myVariants)
        
        
        #print myVariant
            
        #finalIDF = applyTemplates(testIDF, templates)
        
        #print finalIDF

        

    def test0X0_XXX(self):
        print( "**** TEST {} ****".format(get_self()))

class TemplateTtests(unittest.TestCase):
    def setUp(self):
        print( "**** TEST {} ****".format(get_self()))
        #currentPath = split_up_path(__file__)
        thisProjRoot = split_up_path(os.getcwd())[:4] 
        
        
        # Path to XLS definition 
        thisTestExcelProj = "\\".join(thisProjRoot) + r"\ExcelTemplates\Input Data Tower SO03 r06.xlsx"
        self.thisTestExcelProj = thisTestExcelProj
        
        # Path to full IDD
        pathIDDsample2 = thisProjRoot + ["SampleIDFs"] + ["Energy+.idd"]  
        self.pathIDDfull = os.path.join(*pathIDDsample2)
        
        # Path to an actual model file
        path_CentralTower = thisProjRoot + ["SampleIDFs"] + ["r00 MainIDF.idf"]
        self.path_CentralTower = os.path.join(*path_CentralTower)
        
        # Path to IDD XML
        path_IDD_XML = thisProjRoot + ["SampleIDFs"] + ["Energy+idd.xml"]
        self.path_IDD_XML = os.path.join(*path_IDD_XML)
        
    def test050_applyTemplates(self):
        print( "**** TEST {} ****".format(get_self()))
        
        IDDobj = idf.idf_parse.from_XML_file(self.path_IDD_XML)
        print( IDDobj)
        variants = idf.load_cariants(self.thisTestExcelProj)

        # Customize for test
        myVariant = next(iter(variants.values())) # Get one variant
        #pprint((myVariant)#
        myVariant["source"] = self.path_CentralTower # Update source
        myVariant["templates"] = [{'templateName': 'Generic lights', 'zones': '.'}] # Only one template
        myVariants = [myVariant]
        

        
        idf.assemble_variants(myVariants,IDDobj)

class MyTest(unittest.TestCase):
    def test050_applyTemplates(self):
        print( "**** TEST {} ****".format(get_self()))
        testPath = r"C:\Users\Anonymous2\Desktop\TestIDF.txt"
        testPathOUT = r"C:\Users\Anonymous2\Desktop\TestIDF.xml"
        IDFobj = idf.idf_parse.from_IDF_file(testPath)
        IDFobj.write_XML(testPathOUT)
        
        raise
        print( IDDobj)
        variants = idf.load_cariants(self.thisTestExcelProj)

        # Customize for test
        myVariant = next(iter(variants.values())) # Get one variant
        #pprint((myVariant)#
        myVariant["source"] = self.path_CentralTower # Update source
        myVariant["templates"] = [{'templateName': 'Generic lights', 'zones': '.'}] # Only one template
        myVariants = [myVariant]        
         

class JustForCentralDELETEORPHANS(unittest.TestCase):
    def test050_applyTemplates(self):
        print( "**** TEST {} ****".format(get_self()))
        osmFilePath = r"C:\Users\Anonymous2\Desktop\SKPOSM\Main r04.osm"
        osmFileOut = r"C:\Users\Anonymous2\Desktop\SKPOSM\Cleaned.osm"
        IDFobj = idf.idf_parse.from_IDF_file(osmFilePath) 
        idf.delete_orphaned_zones(IDFobj)
        IDFobj.write_IDF(osmFileOut)