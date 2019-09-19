import time
import logging
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


path = os.path.abspath(__file__)

url = r"https://rasp.yandex.ru"
tmp_path = r'\task3'  # Диреткория проекта
log_file = r"\task3.log"  # Название лог файла

go_to = "Переход на сайт %s" % (url)
pro_path = path  # Переменная директории проекта
screen_dir = r"\screen_two"  # Путь директории для скриншотов
os.makedirs( screen_dir, exist_ok=True )  # Если директории для скринов нет, то он её создаст
chrome_driver = 'chromedriver.exe'  # Путь до хромдрайвера
log_path = 'task3_part_two.log'  # Путь до логфайла

name_service = 'Задание 3 часть вторая'

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

        temp_msg = '%s. Заполнение пункта отправления - Кемерово проспект Ленина' % (s)
        kem = browser.find_element_by_xpath('.//*[@id="from"]')
        kem.click()
        kem.clear()
        kem.send_keys(u'Кемерово проспект Ленина')
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Заполнение пункта прибытия - Кемерово Бакинский переулок' % (s)
        msk = browser.find_element_by_xpath('//*[@id="to"]')
        msk.click()
        msk.clear()
        msk.send_keys(u'Кемерово Бакинский переулок')
        s += 1
        logs(ok, temp_msg)


        temp_msg = '%s. Заполнение даты отправки следующая среда' % (s)
        todey = datetime.date.today()
        next_mondey = todey + datetime.timedelta(days=-(todey.weekday()-2),weeks=1)
        sending = browser.find_element_by_xpath('//*[@id="when"]')
        sending.click()
        sending.clear()
        sending.send_keys(str(next_mondey.strftime(("%d.%m.%Y"))))
        sending.send_keys(Keys.ENTER)
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Нажатие кнопки - Автобус ' % (s)
        button = browser.find_element_by_xpath('//*[@id="root"]/div/header/div[1]/div/div[4]/span/label[5]')
        button.click()
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Нажатие кнопки - Найти ' % (s)
        button = browser.find_element_by_xpath('//*[@id="root"]/div/header/div[1]/div/div[5]/form/button[2]')
        button.click()
        s += 1
        logs(ok, temp_msg)

        temp_msg = '%s. Проверка на отображение ошибки ' % (s)
        punkt = browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div[1]/div[1]/div/div[2]/div[2]')
        if 'Пункт прибытия не найден. Проверьте правильность написания или выберите другой город.' not in punkt.text:
            raise Exception('Явная ошибка о некорректном пути приебытия не отображается не отображается')
        s+=1
        logs(ok, temp_msg)

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
