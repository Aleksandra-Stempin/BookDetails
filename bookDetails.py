import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import time
import os
import datetime
import re


class BookDetails():
    driver = None

    def OpenDriver(self):
        """opens driver"""
        global driver
        ChromeDriverPath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        driver = selenium.webdriver.Chrome(ChromeDriverPath)
        driver.implicitly_wait(10)
        driver.maximize_window()

    def GetBookDetails(self, url):
        """gets book details from 'lubimy czytać' web page"""
        global driver
        urlPattern = "https://lubimyczytac.pl/ksiazka/[0-9]+/.+"
        check = re.findall(urlPattern, url)
        check_str = check[0]
        if len(check_str)==len(url) :
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
                try:
                    popUpXpath = '//div[@id="modal1"]//./a[@class="btn btn-primary mb-0 mt-1"]'
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, popUpXpath))).click()
                    print("element found ☺\n")
                except:
                    print("element lost 🙁\n")
                    pass

                # newsletter popup
                try:
                    popup2Tag = 'icon icon-icon-cross'
                    popup2Xpath = '/html/body/div[7]/a/span'
                    popup2Xpath = '//span[@class="icon icon-icon-cross"]'
                    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, popup2Tag))).click()
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, popup2Xpath))).click()
                    print("element ad found ☺\n")
                except:
                    print("element ad lost 🙁\n")
                    pass
                # author
                authorName = ''
                try:

                    authorTag = 'link-name'  # class name
                    authorXpath = '/html/body/div[6]/main/div/section[1]/div/div[2]/div[1]/div[2]/span[1]/a'

                    authorName = ''
                    authors = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located ((By.CLASS_NAME,authorTag)))
                    for author in authors:
                        authorName = authorName + ", " + author.text
                    authorName = authorName.strip(", ")

                    manyAuthorsXpath = '//a[@class="btn-collapse-authors js-btn-collapse-authors collapsed"]'
                    try:
                        manyAuthorsButton = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, manyAuthorsXpath)))
                        manyAuthorsButton.click()
                        moreAuthorsXpath = '//div[@id="authors-list"]/a[@class="link-name"]'
                        moreAuthors = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located ((By.XPATH,moreAuthorsXpath)))
                        for ma in moreAuthors:
                            authorName = authorName + ", " + ma.text
                    except:
                        pass

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
                buttomXpath = '//div[@class="d-flex align-items-center pt-md-3"]/span/button'
                buttom = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, buttomXpath)))
                buttom.click()
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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                errMsg = '''
            Error msg: %s
            Error line no: %s
            Error type: %s
            ''' % (str(e), exc_tb.tb_lineno, exc_type)
                print(errMsg)
                ErrTime = datetime.datetime.now()
                ErrTimeStr = ErrTime.strftime("%Y-%m-%d_%H-%M-%S")
                errPictureName = "error_%s.png" % (ErrTimeStr)
                driver.save_screenshot(errPictureName)
        else:
            print("%s\nwrong url" % (url))

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

    def BookDetailsToFile(self, f_in, dir_out):
        """reads urls from file, gets book details and saves to file in selected folder"""
        bookList = BookDetails.ListFromFile(self, filePath=f_in)
        try:
            booksToFile = ''
            BookDetails.OpenDriver(self)
            for book in bookList:
                try:
                    bookDescription = BookDetails.GetBookDetails(self, book)
                    booksToFile = booksToFile + bookDescription + '\n'
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
            print('booksToFile\n')
            print(booksToFile)
            print("\ngotowe")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errMsg = '''
        Error msg: %s
        Error line no: %s
        Error type: %s
        ''' % (str(e), exc_tb.tb_lineno, exc_type)
            print(errMsg)
            BookDetails.CloseDriver(self)


f_inPath = 'C:/Users/Ola\Desktop/books.txt'
dir_outPath = 'C:/Users/Ola/Desktop/ksiazki'


bd = BookDetails()
# bd.BookDetailsToFile(f_in=f_inPath,
#                      dir_out=dir_outPath)


url = "https://lubimyczytac.pl/ksiazka/4846165/zabojczy-pocisk"
# url = 'https://lubimyczytac.pl/ksiazka/4940609/chodz-za-mna'
bd.OpenDriver()
bookDet = bd.GetBookDetails(url)
print(bookDet)
bd.CloseDriver()