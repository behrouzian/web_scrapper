
import os
from web_scrapping import utils
from web_scrapping.pararius import utils_pararius
from selenium import webdriver
import pandas as pd


if __name__ == "__main__":

    # get the address of current module
    mainScriptPath = os.path.dirname(__file__)
    rawDataPath = os.path.join(mainScriptPath, "rawData\\")
    parariusDataCsvFileName = os.path.join(rawDataPath, "parariusData.csv")
    #create the path if does not exist
    if not os.path.exists(rawDataPath):
        os.makedirs(rawDataPath)

    # get a logger
    logger = utils.get_logger(os.path.basename(parariusDataCsvFileName)
                              , create_file=True, logger_file_Path=rawDataPath)
    logger.info("logging starts ... ")

    # find out if it is a continuation run or new run
    if os.path.isfile(parariusDataCsvFileName):
        # it is a continuation run
        write_header = False
        dfPararius = pd.read_csv(parariusDataCsvFileName,
                                                 delimiter=',')
        allHouseURLList = dfPararius['url'].to_list()
        logger.info("Continuation run! Last iteration: " +
                    str(dfPararius['url'].iloc[-1]))
    else:
        # it is a new run
        logger.info("New run!")
        #create empty datafram
        dfPararius = utils_pararius.get_empty_pararius_dataframe()
        allHouseURLList = []
        write_header = True

    ### OFLINE-ONLINE (DELETE ONCE IN THE NETHERLANDS)
    offlineListPath = "C:\\PythonScripts\\web_scrapping_data\\offline_data\\pararius_list_page1.html"
    soup = utils.make_soup_offline(offlineListPath)

    ######
    #soup = utils.make_soup('https://www.pararius.nl/huurwoningen/nederland/', 'html.parser')

    #get number of pages
    numPages, pagesAdrsTemplate = utils_pararius.how_many_pages(soup)

    ### OFLINE-ONLINE (DELETE ONCE IN THE NETHERLANDS)
    numPages = 1
    ######

    newHouseURLList = []
    stopCounter = 0
    #fast: get the url of all the houses (6 min 10400 houses)
    for numPage in range(1, numPages+1):
        # if the number of the pre-existing houses is more than "stopCounter"
        # it means that we are already in an old list (big number the first time)
        if stopCounter >= 12000:
            break
        try:
            currentPageUrl = pagesAdrsTemplate.replace("pppp", str(numPage))
            currentPageUrl = utils.url_path_join("https://www.pararius.nl/", currentPageUrl)
            ### OFLINE-ONLINE (DELETE ONCE IN THE NETHERLANDS)
            offlineListPath = "C:\\PythonScripts\\web_scrapping_data\\offline_data\\pararius_list_page1.html"
            soup = utils.make_soup_offline(offlineListPath)

            ######
            # soup = utils.make_soup_quick(currentPageUrl)
            for tag in (soup.find_all('li', attrs={"class": "search-list__item search-list__item--listing"})):
                for aTag in tag.find_all('a'):
                    if aTag.has_attr("class"):
                        if any("listing-search-item__link--title" in s for s in aTag['class']):
                            # if the url exist in the registry list add stop counter
                            #otherwise register
                            tempUrl = utils.url_path_join("https://www.pararius.nl/", \
                                                                       aTag['href'])
                            if tempUrl in allHouseURLList:
                                stopCounter = stopCounter + 1
                                break
                            else:
                                newHouseURLList.append(tempUrl)
                                break

        except:
            pass
    logger.info("Number of new houses = {}" .format(len(newHouseURLList)))

    ##get the data of individual houses

    #iterate over new houses
    for currentHouseUrl in newHouseURLList:
        logger.info("get data for : {}" .format(currentHouseUrl))

        ### OFLINE-ONLINE (DELETE ONCE IN THE NETHERLANDS)
        currentHouseUrl = "example"
        offlineIndividualHouseExp = "C:\\PythonScripts\\web_scrapping_data\\offline_data\\pararius_specificHouse_example3.html"
        soup = utils.make_soup_offline(offlineIndividualHouseExp)
        #####
        #soup = utils.make_soup(currentHouseUrl, 'html.parser')

        #first create an empty dictionary given the keys of the parariusParameters
        currentHousedict = utils_pararius.get_empty_pararius_dict()
        currentHousedict = utils_pararius.get_all_data(soup)
        currentHousedict = utils_pararius.clean_house_dict(currentHousedict)
        currentHousedict['url'] = [currentHouseUrl]
        currentHousedf = pd.DataFrame.from_dict(currentHousedict)
        dfPararius.append(currentHousedf)
        currentHousedf.to_csv(parariusDataCsvFileName,index=False, mode='a', header=write_header)
        write_header = False

    #write output
    logger.info("The End!")

    # fetch the info of each house
