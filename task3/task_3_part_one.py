import time
import logging
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


path = os.path.abspath(__file__)

# Path vriables
url = r"https://rasp.yandex.ru"
tmp_path = r'\task3'  # Диреткория проекта
log_file = r"\task3_part_one.log"  # Название лог файла

go_to = "Переход на сайт %s" % (url)
pro_path = path  # Переменная директории проекта
screen_dir = r"\screen"  # Путь директории для скриншотов
os.makedirs( screen_dir, exist_ok=True )  # Если директории для скринов нет, то он её создаст
chrome_driver = 'chromedriver.exe'  # Путь до хромдрайвера
log_path = 'task3_part_one.log'  # Путь до логфайла

name_service = 'Задание 3 часть первая'

# Logginig
logging.basicConfig( handlers=[logging.FileHandler( log_path, "w", "utf-8" )], level=logging.INFO,
                     format="%(message)s" )
log = logging.getLogger( "ex" )


# LogWriter
def logs(stat, msg):
    logging.info( " " + stat + " " + str( msg ) )

ok = " " + "[OK]"
screen = " " + "[SCREEN]"
screen_error = " " + "[SCREEN ERROR]"
error = " " + "[ERROR]"
passed = " " + "[PASSED]"
text_error = " " + "[TEXT ERROR]"
start_log_msg = "-------НАЧАЛО СКРИПТА-------"
end_log_msg = "-------КОНЕЦ СКРИПТА-------"


# Timestamp
def time_fu():
    time_now = datetime.datetime.now()
    temp = (time.mktime( time_now.timetuple() ))
    timestamp_int = int( temp )
    timestamp_int2 = str( timestamp_int )
    return timestamp_int2


# Body script
while True:
    try:
        os.system( 'cls' )

        print( "Путь до автотеста - ", pro_path )
        start_time = int( time_fu() )

        s = 1
        logs( ok, "Путь до автотеста - " + pro_path )
        logs( ok, "Наименование сценария - " + name_service )
        logs( ok, start_log_msg )

        # Start scenario
        temp_msg = "%s. Открытие браузера" %(s)
        browser = webdriver.Chrome(chrome_driver)
        browser.maximize_window()
        browser.get(url)
        s += 1
        logs( ok, temp_msg )

        browser.implicitly_wait(10)#Добавил "неявные ожидания" - ожидает появления какого либо элемента на странице,
                                   #если элемен появится раньше, то скрипт продолжит выполнение шагов

        temp_msg = '%s. Переход на главную страницу' %(s)
        glav = browser.find_element_by_xpath('//*[@id="root"]/div/header/div[1]/div/div[3]/h1')
        if 'Расписание пригородного и междугородного транспорта' not in glav.text:
            raise Exception('Главная страница не открылась')
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Заполнение пункта отправления - Кемерово' % (s)
        kem = browser.find_element_by_xpath('.//*[@id="from"]')
        kem.click()
        kem.clear()
        kem.send_keys(u'Кемерово')
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Заполнение пункта прибытия - Москва' % (s)
        msk = browser.find_element_by_xpath('//*[@id="to"]')
        msk.click()
        msk.clear()
        msk.send_keys(u'Москва')
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Заполнение даты отправки - 07.09.2019' % (s)
        sending = browser.find_element_by_xpath('//*[@id="when"]')
        sending.click()
        sending.clear()
        sending.send_keys(u'07.09.2019')
        sending.send_keys(Keys.ENTER)
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Нажатие кнопки - Найти ' % (s)
        button = browser.find_element_by_xpath('//*[@id="root"]/div/header/div[1]/div/div[5]/form/button[2]')
        button.click()
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Переход на страницу рейсов-проверка названия рейса' % (s)
        the_end = browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div[1]/div[1]/div/div[1]/header/span[1]/h1/span')
        if 'Расписание рейсов из Кемерова в Москву' not in the_end.text:
            raise Exception('Страница с рейсами не отображается')
        s += 1
        logs(ok, temp_msg)

        ############ Пути до всех рейсов + время в полете + пути до иконок##################

        func = browser.find_element_by_xpath
        fly_icon_flight2 = '/header/div/div[1]'
        fly_icon_all = '/div[1]/div[1]/div[2]'
        travel_time_all = '/div[1]/div[2]/div[1]/div[2]'
        travel_time_flight2 ='/div[2]/div[1]/div[2]'
        flight1 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[1]'
        flight2 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/article'
        flight3 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[3]'
        flight4 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[4]'
        flight5 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[5]'
        flight6 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[6]'
        flight7 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[7]'
        flight8 = '//*[@id="root"]/div/main/div/div[1]/div[1]/div/section/div[8]'


        ########################## ПРоверка, что у направления есть время в пути#################################
        temp_msg = "%s. Проверка, что у направления есть время в пути" %(s)
        s += 1
        logs(ok, temp_msg)
        time_flight = 1
        def check_exists_by_xpath(xpath):
            if len(browser.find_elements_by_xpath(xpath)) == True:
                pass
                logs(ok, 'Время рейса ' + str(time_flight) + ' ' + ' отображается корректно')
            else:
                pass
                logs(error, 'Время для рейса '+ str(time_flight) + ' ' + ' НЕ отображается')

        check_exists_by_xpath(flight1 + travel_time_all)
        time_flight += 1
        check_exists_by_xpath(flight2 + travel_time_flight2)
        time_flight += 1
        check_exists_by_xpath(flight3 + travel_time_all)
        time_flight += 1
        check_exists_by_xpath(flight4 + travel_time_all)
        time_flight += 1
        check_exists_by_xpath(flight5 + travel_time_all)
        time_flight += 1
        check_exists_by_xpath(flight6 + travel_time_all)
        time_flight += 1
        check_exists_by_xpath(flight7 + travel_time_all)
        time_flight += 1
        check_exists_by_xpath(flight8 + travel_time_all)
        logs(ok,'_______________________________')

        ################# Проверка на наличие иконки у всех рейсов ##################
        temp_msg = "%s. Проверка, что у всех рейсов есть иконка транспорта." % (s)
        s += 1
        logs(ok, temp_msg)

        time_flight_icon = 1
        def check_exists_by_xpath_icon(xpath):
            if len(browser.find_elements_by_xpath(xpath)) > 0:
                return logs(ok, 'Иконка рейса ' + str(time_flight_icon) + ' ' + ' отображается корректно')
            else:
                pass
                logs(error, 'Иконка рейса ' + str(time_flight_icon) + ' ' + ' НЕ отображается')

        check_exists_by_xpath_icon(flight1 + fly_icon_all)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight2 + fly_icon_flight2)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight3 + fly_icon_all)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight4 + fly_icon_all)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight5 + fly_icon_all)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight6 + fly_icon_all)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight7 + fly_icon_all)
        time_flight_icon += 1
        check_exists_by_xpath_icon(flight8 + fly_icon_all)
        logs(ok, '_______________________________')

        xpath_list = [flight1,
                      flight2,
                      flight3,
                      flight4,
                      flight5,
                      flight6,
                      flight7,
                      flight8
                      ]

        ### Не совсем понимаю, зачем эта проверка, т.к. предыдущие шаги так же проверяют нахождение элементов на странице
        temp_msg = "%s. Проверка, что рейсов отображается - 8" % (s) # В задании сказано - 5, сделал 8 (вероятно опечатка)
        s += 1
        logs(ok, temp_msg)
        d = 0
        for i in xpath_list:
            xpath = browser.find_elements_by_xpath(i)
            d += 1
            if len(xpath) == True:
                logs(ok, 'Рейс: '+ str(d) + ' отображается')
            else:
                pass
                logs(error, "На странице отображаются не все рейсы")


        temp_msg = "%s. Закрытие браузера" %(s)
        browser.close()
        browser.quit()
        s += 1
        logs( ok, temp_msg )

        # End scenario
        end_time = int(time_fu()) - start_time
        logs( ok, end_log_msg )
        logging.info( " " + passed + ' ' + "Время выполнения скрипта - " + str( end_time ) + ' секунд')
        del start_time, end_time, temp_msg, s

        logging.shutdown()



    except FileNotFoundError:
        pass

    except (Exception) as err:
        # Screenshot
        todey = datetime.datetime.today()
        date_time_mow = todey.strftime("%Y-%m-%d-%H.%M.%S")
        try:
            browser.save_screenshot( screen_path + date_time_mow+'.png')
            time.sleep(3)
            print("Сделан скриншот в директории - ", screen_dir)

        except Exception as t:
            logging.error(time_fu() + " " + screen_error + " " + str( 'Ошибка скриншота' ) )

        # Format print error
        format_error = str( err ).split( '/b' )
        print( error + " " + str( temp_msg ) )
        print( text_error + " " + str( format_error ) )
        browser.quit()

        # Format logging error
        logging.error(error + " " + str( temp_msg ) )
        logging.error(text_error + " " + str( format_error ) )
        logging.info(screen + " " +  " Сделан скриншот в директории - " + str(screen_dir))

        # Script time
        end_time = int( time_fu() ) - start_time
        print( "Время выполнения скрипта - ", end_time )
        logging.error( " " + str( end_time ) )

        # Exit
        logging.shutdown()
        del err
        del start_time, end_time, temp_msg
        time.sleep( 1 )




    finally:
        print('Скрипт завершил свою работу')
    time.sleep( 30 )
