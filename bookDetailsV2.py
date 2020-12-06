import selenium
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys
import time
import os
import datetime
import re


class BookDetails():
    driver = None
    fileIn = None
    directoryOut = None



    def OpenDriver(self):
        """opens driver"""
        global driver
        ChromeDriverPath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        driver = selenium.webdriver.Chrome(ChromeDriverPath)
        driver.implicitly_wait(10)
        driver.maximize_window()

    def GetBookDetails(self, url, directory_out):
        """gets book details from 'lubimy czytać' web page"""
        errFolder = "%s/ErrorsScreenShots" % (directory_out)
        errFolder = "%s/ErrorsScreenShots" % (directory_out)
        urlPattern = "https://lubimyczytac.pl/ksiazka/[0-9]+/.+"
        check = re.findall(urlPattern, url)
        check_str = check[0]
        if len(check_str)==len(url) :
            action = ActionChains(driver)
            try:
                driver.get(url)
                time.sleep(3)

                # zoom popup
                try:
                    zoomXpath = '//a[@class="btn btn-primary mb-0 mt-1 js-close-zoom-btn"]'
                    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, zoomXpath))).click()
                except:
                    pass

                # adverts popup

                # try:
                #     popUpXpath = '//div[@id="modal1"]//./a[@class="btn btn-primary mb-0 mt-1"]'
                #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, popUpXpath))).click()
                # # except TimeoutException as ex:
                # #     popUpXpath2 = '//div[@id="modal - content"]//./a[@class="btn btn-primary mb-0 mt-1"]'
                # #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, popUpXpath2))).click()
                # except:
                #     pass

                try:

                    # popUpXpath = '//a[@class="btn btn-primary mb-0 mt-1"]'
                    popUpXpath = '//button[@class="close"]'
                    popUpClass = 'btn btn-primary mb-0 mt-1'
                    adButtons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, popUpXpath)))
                    # addButtons = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_all_elements_located((By.CLASS_NAME, popUpClass)))


                    for adButton in adButtons:
                        try:
                            # print("next addButton %s"%(str(adButton)))
                            # addButton.click()
                            action.move_to_element(adButton).click().perform()
                            action.move_to_element(adButton).click().perform()
                            action.move_to_element(adButton).click().perform()
                            # print("znalazlem")
                            # action.click(on_element=adButton)
                            # action.perform()
                            # print("button clicked")
                            break
                        except:
                            continue
                    # print("koniec klikania")
                except:
                    pass

                # newsletter popup
                try:
                    popup2Tag = 'icon icon-icon-cross'
                    popup2Xpath = '/html/body/div[7]/a/span'
                    popup2Xpath = '//span[@class="icon icon-icon-cross"]'
                    popup2Xpath = '//a[@class="footer__fixed__close js-footer-fixed-close-btn pl-3 pb-3"]'
                    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, popup2Tag))).click()
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, popup2Xpath))).click()
                    # popup2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, popup2Xpath)))
                    # action.move_to_element(popup2).click().perform()
                    # action.move_to_element(popup2).click().perform()
                    # action.move_to_element(popup2).click().perform()
                    # print("newsletter popup clicked")
                except Exception as e:
                    print("popup2", str(e))
                    pass
                # author
                authorName = ''
                try:
                    authorTag = 'link-name'  # class name
                    authorXpath = '/html/body/div[6]/main/div/section[1]/div/div[2]/div[1]/div[2]/span[1]/a'
                    manyAuthorsXpath = '//a[@class="btn-collapse-authors js-btn-collapse-authors collapsed"]'
                    try:
                        manyAuthorsButton = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, manyAuthorsXpath)))
                        manyAuthorsButton.click()
                    except:
                        pass

                    authorName = ''
                    authors = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located ((By.CLASS_NAME,authorTag)))
                    for author in authors:
                        authorName = authorName + ", " + author.text
                    authorName = authorName.strip(", ")


                except:
                    authorName = 'no author'

                # title
                bookTitle = ''
                try:
                    titleTag = 'book__title js-book-title-scale'  # class
                    titleXpath = '//*[@id="book-info"]/div/h1'
                    title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, titleXpath)))
                    bookTitle = title.text
                except:
                    bookTitle = 'noTitle'
                # serie
                serieName = ''
                try:
                    # serieXpath = '/html/body/div[6]/main/div/section[1]/div/div[2]/div[1]/div[2]/span[3]/a'
                    serieXpath = '//span[@class="d-none d-sm-block mt-1"]/a'
                    serie = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, serieXpath)))
                    serieName = serie.text
                except:
                    serieName = '-'
                # genre
                genreName = ''
                try:
                    genreTag = 'book__category d-sm-block d-none'  # class
                    genreXpath = '//a[@class="book__category d-sm-block d-none"]'
                    genre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, genreXpath)))
                    genreName = genre.text
                except:
                    genreName = 'no genre'
                # publisher
                publisherName = ''
                try:

                    publisherXpath = '/html/body/div[6]/main/div/section[1]/div/div[2]/div[1]/div[2]/span[2]/a'

                    publisherXpath = '//span[@class="book__txt d-lg-inline-block mt-2 "]/a'
                    publisher = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, publisherXpath)))
                    publisherName = publisher.text
                except:
                    publisherName = 'no publisher'
                # bottom details
                try:
                    buttonDetXpath = '//div[@class="d-flex align-items-center pt-md-3"]/span/button'
                    buttonDetXpath = '//div[@class="d-flex align-items-center pt-md-3"]/.//button'
                    # buttonDet = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, buttonDetXpath)))
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, buttonDetXpath))).click()
                    # buttonDet = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, buttonDetXpath)))
                    # action.move_to_element(buttonDet).click().perform()
                    # action.move_to_element(buttonDet).click().perform()
                    # action.move_to_element(buttonDet).click().perform()
                    # buttom.click()
                    # print('bottom details clicked')
                except Exception as e:
                    print('buttonDet', str(e))
                    pass
                time.sleep(3)

                # language
                lang = ''
                try:
                    langXpath = '//dl/dt[contains(text(),"Język:")]/following-sibling::dd'
                    lang = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, langXpath))).text
                except:
                    lang = 'no language'

                # original title
                orgTitle = ''
                try:
                    try:
                        orgTitleXpath = '//dl/dt[contains(text(),"Tytuł oryginału:")]/following-sibling::dd'
                        orgTitle = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, orgTitleXpath))).text
                    except:
                        orgTitle = bookTitle
                except:
                    orgTitle = 'no original title'

                # isbn
                ISBN = ''
                try:
                    isbnXpath = '//dl/dt[contains(text(),"ISBN:")]/following-sibling::dd'
                    ISBN = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, isbnXpath))).text
                except:
                    ISBN = "no ISBN"

                booKDetailsLine = '%s;%s;%s;%s;%s;%s;%s;%s' % (authorName, bookTitle, orgTitle, serieName, genreName,
                                                               publisherName, lang, ISBN)

                time.sleep(1)
                return booKDetailsLine
            except Exception as e:
                if not os.path.isdir(errFolder):
                    os.mkdir(errFolder)
                ErrTime = datetime.datetime.now()
                ErrTimeStr = ErrTime.strftime("%Y-%m-%d_%H-%M-%S")
                errPictureName = "%s/error_%s.png" % (errFolder, ErrTimeStr)
                # print(errPictureName)
                driver.save_screenshot(errPictureName)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                errMsg = '''
Get book details

Error msg: %s
Error line no: %s
Error type: %s
            ''' % (str(e), exc_tb.tb_lineno, exc_type)
                print(errMsg)

        else:
            print("%s\nwrong url" % (url))

    def GetBookDetailsFromGR(self, url, directory_out):
        global driver
        errFolder = "%s/ErrorsScreenShots" % (directory_out)
        urlPattern = "https://www.goodreads.com/book/show/[0-9]+"
        if re.findall(urlPattern, url):
            try:
                driver.get(url)
                # pop up
                try:
                    popUpXpath = '//div[@class="modal__content"]/div[@class="modal__close"]/button[@class="gr-iconButton"]'
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, popUpXpath))).click()
                except:
                    pass
                # bookAuthor
                authorsNames = ''
                try:
                    authorsXpath = '//div[@id="bookAuthors"]/.//span[@itemprop="name"]'
                    authors = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, authorsXpath)))
                    for author in authors:
                        authorsNames = authorsNames + author.text + ', '
                    try:
                        # transtlatorXpath = '//div[@id="bookAuthors"]/.//div[@class="authorName__container"]/.//span[contains(text(), "(Translator)")]/preceding-sibling::a/span'
                        otherXpath = '//span[@class="authorName greyText smallText role"]/preceding-sibling::a/span'
                        otherPeople =  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, otherXpath)))
                        others = ''
                        for person in otherPeople:
                            others = others + person.text + ', '

                        authorsNames = authorsNames.replace(others, "")
                        # print(translator)
                    except:
                        pass
                    authorsNames = authorsNames.strip(', ').strip(' ')
                except:
                    authorsNames = "no author"

                # bookTitle
                try:
                    titleID = "bookTitle"
                    bookTitle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, titleID))).text
                    bookTitle = bookTitle.strip()
                except:
                    bookTitle = "no title"

                # publisher
                try:
                    publisherXpath = '//div[@class="row" and contains(text(),"Published")]'#/text()'
                    publisher = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, publisherXpath))).text
                    publisherName = publisher.split("by")[1]
                    publisherName = publisherName.split("(")[0]
                    publisherName = publisherName.strip()
                except:
                    publisherName = "no publisher"


                # more details button
                try:
                    moreDetailsButXpath = ''
                    moreDetailsButID = 'bookDataBoxShow'
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, moreDetailsButID))).click()
                except:
                    pass
                # original title
                originalTitle =""
                try:
                    originalTitleXpath = '//div[@id="bookDataBox"]/.//div[contains(text(),"Original Title")]/following-sibling::div'
                    originalTitle = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, originalTitleXpath))).text
                    originalTitle = originalTitle.strip()
                except:
                    originalTitle = bookTitle


                # series
                series = ''
                try:
                    seriesXpath = '//div[@class="infoBoxRowItem"]/a[contains(@href, "series")][1]'
                    series = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, seriesXpath))).text
                    series = series.strip()
                except:
                    series = '-'

                # language
                language = ''
                try:
                    languageXpath = '//div[@itemprop="inLanguage"]'
                    language = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, languageXpath))).text
                    language=language.strip()
                except:
                    language = 'no language'

            # genre
                genres = []
                try:
                    genreXpath = '//div[@class="elementList "]/div[@class="left"]'
                    genresList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, genreXpath)))
                    for genre in genresList:
                        genres.append(genre.text)
                except:
                    genres.append("no genre")
                if len(genres)>2:
                    genres = genres[0:2]
                bookGenres = ''
                for g in genres:
                    bookGenres = bookGenres + g + ', '
                bookGenres = bookGenres.strip(", ").strip(' ')

                # ISBN
                ISBN = ''
                try:
                    isbnXpath = '//span[@itemprop="isbn"]'
                    ISBN = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located ((By.XPATH, isbnXpath))).text
                    ISBN = ISBN.strip()
                except:
                    ISBN = 'no ISBN'
                # time.sleep(1)
                bookDet = '%s;%s;%s;%s;%s;%s;%s;%s'%(authorsNames, bookTitle, originalTitle, series, bookGenres, publisherName, language,ISBN)
            except Exception as e:
                if not os.path.isdir(errFolder):
                    os.mkdir(errFolder)
                ErrTime = datetime.datetime.now()
                ErrTimeStr = ErrTime.strftime("%Y-%m-%d_%H-%M-%S")
                errPictureName = "%s/error_%s.png" % (errFolder, ErrTimeStr)
                # print(errPictureName)
                driver.save_screenshot(errPictureName)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                errMsg = '''
                                                     Get book details GoodReaders

                                                     Error msg: %s
                                                     Error line no: %s
                                                     Error type: %s
                                                                 ''' % (str(e), exc_tb.tb_lineno, exc_type)
                print(errMsg)

        else:
            bookDet = ""
            print("wrong url")
        return bookDet
    def CloseDriver(self):
        """closes driver"""
        global driver
        driver.close()
        driver.quit()

    def ListFromFile(self, filePath):
        """prepares list from a file"""
        try:
            # open file
            listFromFile = []
            f = open(filePath, "rt")
            for line in f:
                line = line.strip()
                listFromFile.append(line)
            f.close()
            return listFromFile
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errMsg = '''
        Error msg: %s
        Error line no: %s
        Error type: %s
        ''' % (str(e), exc_tb.tb_lineno, exc_type)
            print(errMsg)
            return []

    def BookDetailsToFileGoodReaders(self, f_in, dir_out):
        """reads urls from file, gets book details and saves to file in selected folder"""
        bookList = BookDetails.ListFromFile(self, filePath=f_in)
        try:
            booksToFile = ''
            BookDetails.OpenDriver(self)
            for book in bookList:
                try:
                    bookDescription = BookDetails.GetBookDetailsFromGR(self, book, dir_out)
                    booksToFile = booksToFile + bookDescription + '\n'
                    print(bookDescription)
                except:
                    print("wywala się\n"+str(book))
                    continue
            BookDetails.CloseDriver(self)
            currTime = datetime.datetime.now()
            currTimeStr = currTime.strftime("%Y-%m-%d_%H-%M-%S")
            fileName = "%s/books_%s.txt" % (dir_out, currTimeStr)
            fOut = open(fileName, "w")
            fOut.write(booksToFile)
            fOut.close()
            # print('booksToFile\n')
            # print(booksToFile)
            print("\ngotowe")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errMsg = '''
BookDetailsToFile

Error msg: %s
Error line no: %s
Error type: %s
        ''' % (str(e), exc_tb.tb_lineno, exc_type)
            print(errMsg)
            BookDetails.CloseDriver(self)

    def BookDetailsToFile(self, f_in, dir_out):
        """reads urls from file, gets book details and saves to file in selected folder"""
        bookList = BookDetails.ListFromFile(self, filePath=f_in)
        try:
            booksToFile = ''
            BookDetails.OpenDriver(self)
            print("\nbook details\n")
            for book in bookList:
                try:
                    bookDescription = BookDetails.GetBookDetails(self, book, dir_out)
                    booksToFile = booksToFile + bookDescription + '\n'
                    print(bookDescription)
                except:
                    print("wywala się\n" + str(book))
                    continue
            BookDetails.CloseDriver(self)
            currTime = datetime.datetime.now()
            currTimeStr = currTime.strftime("%Y-%m-%d_%H-%M-%S")
            fileName = "%s/books_%s.txt" % (dir_out, currTimeStr)
            fOut = open(fileName, "w")
            fOut.write(booksToFile)
            fOut.close()
            # print('booksToFile\n')
            # print(booksToFile)
            print("\ngotowe")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errMsg = '''
BookDetailsToFile

Error msg: %s
Error line no: %s
Error type: %s
        ''' % (str(e), exc_tb.tb_lineno, exc_type)
            print(errMsg)
            BookDetails.CloseDriver(self)


f_inPath = 'C:/Users/Ola\Desktop/books.txt'

dir_outPath = 'C:/Users/Ola/Desktop/ksiazki'


bd = BookDetails()
#ang
# bd.BookDetailsToFileGoodReaders(f_in=f_inPath,
#                      dir_out=dir_outPath)
#pol

bd.BookDetailsToFile(f_in=f_inPath,
                     dir_out=dir_outPath)

# bd = BookDetails()
# url = "https://lubimyczytac.pl/ksiazka/4846165/zabojczy-pocisk"
# url = 'https://lubimyczytac.pl/ksiazka/4127349/dobroc-nieznajomych'
# urlAng = 'https://www.goodreads.com/book/show/6043781-blood-of-elves'
# urlAng = 'https://www.goodreads.com/book/show/43299138-the-last-paper-crane'
# urlAng = "https://www.goodreads.com/book/show/7128341-the-prince-of-mist"
# urlAng = 'https://www.goodreads.com/book/show/6043781-blood-of-elves'
# urlAng = 'https://www.goodreads.com/book/show/23278280-off-the-page'
# urlAng = 'https://www.goodreads.com/book/show/53478680-the-magic-book'
# bd.OpenDriver()
# bookDet = bd.GetBookDetails(url, dir_outPath )
# bookDet = bd.GetBookDetailsFromGR(urlAng, dir_outPath)
# print("\nbookDet", bookDet)
# bd.CloseDriver()

input("pres ENTER to finish")
