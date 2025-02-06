import os
import json
import configparser
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, JavascriptException
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

# Konfigurationsdatei laden
config = configparser.ConfigParser()
config.read('config.ini')

username = config['login']['username']
password = config['login']['password']

# Selenium Optionen setzen
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: im Hintergrund ausführen
chrome_options.add_argument("--disable-gpu")

# Webdriver initialisieren
driver = webdriver.Chrome(options=chrome_options)

def scrape_website():
    try:
        # Webseite öffnen
        driver.get("https://mk-navi.mebis.bycs.de/mctool/mymc")

        # Login durchführen
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-username"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-password"))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-do-log-in"))).click()

        # Auf die nächste Seite warten
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fa-light.fa-link")))

        # Cookies und Session-Informationen extrahieren
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # API-URL aufrufen
        api_url = "https://mk-navi.mebis.bycs.de/api/mcs"
        response = session.get(api_url)
        response.raise_for_status()  # Fehler auslösen, wenn der HTTP-Statuscode ein Fehler ist

        # JSON-Antwort verarbeiten
        data = response.json()
        items = data.get('collection', {}).get('items', [])

        # IDs extrahieren und Embedd-Links, Focalpoints und Suggestions abrufen
        for item in items:
            id = item['href'].split('/')[-1]
            
            # Profession Title und Title extrahieren
            profession_title = None
            title = None
            for data_item in item.get('data', []):
                if data_item['name'] == 'profession_title':
                    profession_title = data_item['value']
                elif data_item['name'] == 'title':
                    title = data_item['value']
            
            if not profession_title or not title:
                continue  # Falls die erforderlichen Daten fehlen, überspringen

            # Ungültige Zeichen im Dateinamen ersetzen
            safe_title = title.replace(':', '_').replace('/', '_').replace('\\', '_')
            safe_profession_title = profession_title.replace(':', '_').replace('/', '_').replace('\\', '_')

            # Verzeichnis und Dateinamen festlegen
            base_directory = os.path.join("export", safe_profession_title)
            if not os.path.exists(base_directory):
                os.makedirs(base_directory)
            filename = os.path.join(base_directory, f"{safe_title}.json")

            # Embedd-Link abrufen
            embedd_url = f"https://mk-navi.mebis.bycs.de/api/mcs/{id}/embeddlink"
            embedd_response = session.get(embedd_url)
            embedd_response.raise_for_status()
            embedd_data = embedd_response.json()

            # Focalpoints abrufen
            focalpoints_url = f"https://mk-navi.mebis.bycs.de/api/mcs/{id}/focalpoints"
            focalpoints_response = session.get(focalpoints_url)
            focalpoints_response.raise_for_status()
            focalpoints_data = focalpoints_response.json()

            # Suggestions abrufen
            suggestions_url = f"https://mk-navi.mebis.bycs.de/api/mcs/{id}/suggestions"
            suggestions_response = session.get(suggestions_url)
            suggestions_response.raise_for_status()
            suggestions_data = suggestions_response.json()

            # Daten in eine Datei speichern
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "embedd_data": embedd_data,
                    "focalpoints_data": focalpoints_data,
                    "suggestions_data": suggestions_data
                }, f, ensure_ascii=False, indent=4)

            print(f"Daten für '{title}' in '{filename}' gespeichert.")

    except TimeoutException:
        print("Ein Timeout-Fehler ist aufgetreten.")
    except ElementNotInteractableException:
        print("Ein Element konnte nicht interagiert werden.")
    except JavascriptException as e:
        print(f"Ein JavaScript-Fehler ist aufgetreten: {e}")
    except requests.RequestException as e:
        print(f"Ein Fehler bei der API-Anfrage ist aufgetreten: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_website()