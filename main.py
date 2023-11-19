from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pytz

# Параметр времени ожидания. Если есть ошибки, можно с ним поиграться
WAIT_TIME = 10
# Получение непосредственной даты следущей недели. Если есть ошибки на стадии закачки - может помочь
# DATE = str(datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg')) + datetime.timedelta(days=7))[:10]

# Обе папки нужно предварительно создать
# Папка для временного хранения расписания, чтобы скачать его и привести в надлежащее состояние
download_dir =  r'C:\DIR\TO\DIRECTORY\DOWNLOAD\FILE'
# Папка, где будет храниться файл календаря и его название
ics_dir = r'C:\DIR\TO\CALENDAR\FILE\FILE_NAME.ics'

# Данные для входа в Модеус
login_tyuiu = 'YOUR_LOGIN@std.tyuiu.ru'
password_tyuiu = 'YOUR_PASSWORD'

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
# Изменение опций загрузки
options.add_experimental_option(
    'prefs',
    {
          'download.default_directory': download_dir,
          'download.prompt_for_download': False,
          'download.directory_upgrade': True,
          'safe_browsing.enabled': True
    }
)

# Непосредственный вход в Модеус
driver = webdriver.Chrome(options=options)
driver.get('https://tyuiu.modeus.org/')

# Страница выбора типа учётной записи
driver.implicitly_wait(WAIT_TIME)
driver.find_elements(By.CLASS_NAME, 'idp')[1].click()

# Страница авторизации
driver.implicitly_wait(WAIT_TIME)
driver.find_element(By.ID, 'userNameInput').send_keys(login_tyuiu)
driver.find_element(By.ID, 'passwordInput').send_keys(password_tyuiu)
driver.find_element(By.ID, 'submitButton').click()

# Скачивание календаря на след неделю
# Прямой переход на страницу с расписание. Если есть ошибки на стадии закачки - может помочь.
# driver.get('https://tyuiu.modeus.org'
#            '/schedule-calendar/my?timeZone=%22Asia%2FTyumen%22&calendar=%7B%22view%22:%22agendaWeek%22,'
#            '%22date%22:%22'
#            f'{DATE}'
#            'T13:23:12%22%7D')

WebDriverWait(driver, WAIT_TIME).until(
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
if os.path.exists(ics_dir):
    os.remove(ics_dir)
with open(ics_dir, 'w', encoding="utf-8") as ics:
    ics.write(week)
