import pandas as pd
import re

parariusParameters = {'rentPriceStr':["dd", "listing-features__description--for_rent_price"],
'inclusive':["dd", "listing-features__description--for_rent_price"],
'dwelling_type':["dd", "listing-features__description--dwelling_type"],
'number_of_rooms':["dd", "listing-features__description--number_of_rooms"],
'facilities':["dd", "listing-features__description--facilities"],
'energy-label':["dd", "listing-features__description--energy-label"],
'storage':["dd", "listing-features__description--storage"],
'surface_area':["dd", "listing-features__description--surface_area"],
'location':["div", "listing-detail-summary__location"],
'title':["h1", "listing-detail-summary__title"],
'offeredSince':["dd", "listing-features__description--offered_since"],
'availableFrom':["dd", "listing-features__description--acceptance"],
'contractDuration':["dd", "listing-features__description--contract_duration"],
'parkingPlacePresent':["dd", "listing-features__description--available"],
'url':["dd", "amir"],
                      }

def get_empty_pararius_dict():
    emptyDict = dict()
    for item in parariusParameters.keys():
        emptyDict[str(item)] = "-"
    return emptyDict

def get_empty_pararius_dataframe():
    df = pd.DataFrame()
    for key in get_empty_pararius_dict():
        df[key] = "-"
    return df

def get_all_data(soup):
    tempDict = get_empty_pararius_dict()
    for key in parariusParameters.keys():
        for tag in soup.find_all(parariusParameters[key][0]):
            if tag.has_attr("class"):
                if any(parariusParameters[key][1] in s for s in tag['class']):
                    tempDict[key] = [tag.get_text()]
    return tempDict

def clean_house_dict(tempDict):
    # if tempDict['rentalPriceStr'] contains "inclusief/exclusief" data
    if ("inclusief" in tempDict['rentPriceStr'][0].lower()) |\
            ("exclusief" in tempDict['rentPriceStr'][0].lower()):
        inclusiveDataStartCharacterPosition = len(tempDict['rentPriceStr'][0])
        exclusiveDataStartCharacterPosition = len(tempDict['rentPriceStr'][0])
        if "inclusief" in tempDict['rentPriceStr'][0].lower():
            #find where the position of 'inclusive/exclusive' data starts
            inclusiveDataStartCharacterPosition = re.search(r"inclusief:",
                                                            tempDict['rentPriceStr'][0].lower()).start()
        if "exclusief" in tempDict['rentPriceStr'][0].lower():
            exclusiveDataStartCharacterPosition = re.search(r"exclusief:",
                                                            tempDict['rentPriceStr'][0].lower()).start()
        startPosition = min(inclusiveDataStartCharacterPosition,
                                exclusiveDataStartCharacterPosition)
        tempDict['inclusive'][0] = tempDict['rentPriceStr'][0][startPosition:]

    # remove dot from the price
    tempDict['rentPriceStr'][0] = tempDict['rentPriceStr'][0].replace(".", "")

    # extract only numbers from rentPriceStr
    pattern = r'\d+'
    pattern_regex = re.compile(pattern)
    result = pattern_regex.findall(tempDict['rentPriceStr'][0].lower())
    # if the result makes sense
    if (int(result[0]) >= 300) & (int(result[0]) <= 10000):
        tempDict['rentPriceStr'][0] = str(result[0])

    return tempDict


def get_rent_price(soup):

    # rentPrice
    for tag in soup.find_all('dd'):
        if tag.has_attr("class"):
            if any("listing-features__description--for_rent_price" in s for s in tag['class']):
                if len(tag.find_all('div')) > 0:
                    for nieuwDivTag in tag.find_all('div'):
                        if tag.has_attr("class"):
                            if any("listing-features__main-description" in s for s in nieuwDivTag['class']):
                                try:
                                    return ([nieuwDivTag.get_text()],
                                           [nieuwDivTag.get_text().split()[1]],
                                           [nieuwDivTag.get_text().split()[3]])
                                except:
                                    return (["NaN"],
                                            ["NaN"],
                                            ["NaN"])
                elif len(tag.find_all('span')) > 0:
                    try:
                        return ([tag.get_text(),]
                                [tag.get_text().split()[1]],
                                [tag.get_text().split()[3]])
                    except:
                        try:
                            return ([tag.get_text()],
                                ["NAN"],
                                ["NAN"])
                        except:
                            return (["NaN"],
                             ["NaN"],
                             ["NaN"])
                else:
                    return (["NaN"],
                            ["NaN"],
                            ["NaN"])

def get_main_page(soup):
    # rentPrice
    for tag in soup.find_all(parariusParameters['main'][0]):
        if tag.has_attr("class"):
            if any(parariusParameters['main'][1] in s for s in tag['class']):
                return [str(tag)]


def how_many_pages(soup):
    pageNumberList = []
    firstIteration = True
    for tag in soup.find_all('a'):
        if tag.has_attr("class"):
            if any("pagination__link" in s for s in tag['class']):    # tag['calss'] is a list
                pageNumberList.append(int(tag['data-pagination-page']))
                if firstIteration:
                    #take the page template
                    pagesAdrsTemplate = str(tag['href'])
                    pagesAdrsTemplate = pagesAdrsTemplate.replace(str(int(tag['data-pagination-page'])), "pppp")
                    firstIteration = False

    return (max(pageNumberList), pagesAdrsTemplate)




