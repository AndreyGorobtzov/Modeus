from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pytz

WAIT_TIME = 1
DATE = str(datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg')) + datetime.timedelta(days=7))[:10]
download_dir = r'C:\Users\Andrey\Desktop\Modeus\files'

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

options.add_experimental_option(
    'prefs',
    {
          'download.default_directory': download_dir,
          'download.prompt_for_download': False,
          'download.directory_upgrade': True,
          'safe_browsing.enabled': True
    }
)

login_tyuiu = 'gorobtsovaa@std.tyuiu.ru'
password_tyuiu = 'AndreyAG2142!'

driver = webdriver.Chrome(options=options)
driver.get('https://tyuiu.modeus.org/')

# Страница выбора типа учётной записи
driver.implicitly_wait(WAIT_TIME)
driver.find_elements(By.CLASS_NAME, 'idp')[1].click()

# Страница ввода данных
driver.implicitly_wait(WAIT_TIME)
driver.find_element(By.ID, 'userNameInput').send_keys(login_tyuiu)
driver.find_element(By.ID, 'passwordInput').send_keys(password_tyuiu)
driver.find_element(By.ID, 'submitButton').click()

# Скачивание календаря на след неделю
driver.get('https://tyuiu.modeus.org'
           '/schedule-calendar/my?timeZone=%22Asia%2FTyumen%22&calendar=%7B%22view%22:%22agendaWeek%22,'
           '%22date%22:%22'
           f'{DATE}'
           'T13:23:12%22%7D')

WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.icon-icalendar'
            )
        )
).click()

driver.quit()

# Работа с файлом
import glob
import os

with open(max(glob.glob('files/*'), key=os.path.getctime), encoding="utf8") as ics:
    week = list(ics.read().split('\n'))

for filename in os.listdir(download_dir):
    file_path = os.path.join(download_dir, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f'Ошибка при удалении файла {file_path}. {e}')

week = [
    x
    for x in week
    if
    'DESCRIPTION' not in x and
    'ORGANIZER' not in x and
    'SEQUENCE' not in x and
    'CATEGORIES' not in x
]

for i in range(len(week)):
    if 'SUMMARY' in week[i]:
        week[i] = 'SUMMARY:' + week[i].split(' / ')[-1]
    if 'LOCATION' in week[i]:
        week[i] = 'LOCATION:' + week[i].split(' / ')[-1]

week = '\n'.join(week)
if os.path.exists(r'C:\Users\Andrey\Desktop\FILE_MODEUS\next_week.ics'):
    os.remove(r'C:\Users\Andrey\Desktop\FILE_MODEUS\next_week.ics')
with open(r'C:\Users\Andrey\Desktop\FILE_MODEUS\next_week.ics', 'w', encoding="utf-8") as ics:
    ics.write(week)