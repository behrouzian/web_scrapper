
import os
from web_scrapping import utils
from web_scrapping.pararius import utils_pararius
from selenium import webdriver
import pandas as pd


if __name__ == "__main__":

    # get the address of current module
    mainScriptPath = os.path.dirname(__file__)
    rawDataPath = os.path.join(mainScriptPath, "rawData\\")
    parariusDataCsvFileName =  os.path.join(rawDataPath, "parariusData.csv")
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

    soup = utils.make_soup('https://www.pararius.nl/huurwoningen/nederland/', 'html.parser')

    #get number of pages
    numPages, pagesAdrsTemplate = utils_pararius.how_many_pages(soup)

    newHouseURLList = []
    #if the
    stopCounter = 0
    #fast: get the url of all the houses (6 min 10400 houses)
    for numPage in range(1, numPages):
        if stopCounter >= 12000:
            break
        try:
            newHouseExist = False
            #logger.info("number of urls: " .format(len(allHousesUrlList)))
            currentPageUrl = pagesAdrsTemplate.replace("pppp", str(numPage))
            currentPageUrl = utils.url_path_join("https://www.pararius.nl/", currentPageUrl)
            soup = utils.make_quick_soup(currentPageUrl)
            for tag in (soup.find_all('li', attrs={"class": "search-list__item search-list__item--listing"})):
                for aTag in tag.find_all('a'):
                    if aTag.has_attr("class"):
                        if any("listing-search-item__link--title" in s for s in aTag['class']):
                            # if the url exist in the registery list add stop counter
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



    #create the url list of new houses
    newHouseURLList = []
    # iterate over pages as long as the item are "nieuw"
    for numPage in range(1,numPages):
        newHouseURLList = []
        newHouseExist = False
        currentPageUrl = pagesAdrsTemplate.replace("pppp", str(numPage))
        currentPageUrl = utils.url_path_join("https://www.pararius.nl/", currentPageUrl )
        soup = utils.make_soup(currentPageUrl, 'html.parser')

        dfPararius['url'].iloc[-1]
        #get data of last house in the last fetch

        #convert the

        newHouseURLList = utils_pararius.get_new_house_list
        #iterate over the items with the tag new
        for tag in (soup.find_all('li', attrs={"class": "search-list__item--listing"})):
            for nieuwSpanTag in tag.find_all('span'):
                if tag.has_attr("class"):
                    #if any("listing-search-item__is-new" in s for s in nieuwSpanTag['class']):
                    if True:
                        for nieuwH2Tag in tag.find_all('a'):
                            if nieuwH2Tag.has_attr("class"):
                                if any("listing-search-item__link--title" in s for s in nieuwH2Tag['class']):
                                    newHouseURLList.append(utils.url_path_join("https://www.pararius.nl/", \
                                                                               nieuwH2Tag['href']))
                                    newHouseExist = True
        if not newHouseExist:
            break
        logger.info("Number of new houses = {}" .format(len(newHouseURLList)))
        #check if the houses data is already recorded
        for currentHouseUrl in newHouseURLList:
            if not dfPararius['url'].str.contains(currentHouseUrl).any():
                logger.info("get data for : {}" .format(currentHouseUrl))
                soup = utils.make_soup(currentHouseUrl, 'html.parser')
                currentHousedict = utils_pararius.get_empty_pararius_dict()

                # currentHousedict['rentPriceStr'],\
                # currentHousedict['rentPrice'], \
                # currentHousedict['pricePeriod']= utils_pararius.get_rent_price(soup)
                # logger.info("rentPriceStr: {}".format(currentHousedict['rentPriceStr']))
                currentHousedict = utils_pararius.get_all_data(soup)
                currentHousedict['url'] = [currentHouseUrl]
                currentHousedf = pd.DataFrame.from_dict(currentHousedict)
                dfPararius.append(currentHousedf)
                currentHousedf.to_csv(parariusDataCsvFileName,index=False, mode='a', header=write_header)
                write_header = False

    #write output
    logger.info("The End!")

    # fetch the info of each house
