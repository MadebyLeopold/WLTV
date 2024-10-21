import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Liste der URLs, die getestet werden sollen
urls = [
    "https://www.juzztfriends.de/",
    # Füge hier weitere URLs hinzu
]

# Dictionary zum Speichern der Ladezeiten
load_times = {url: [] for url in urls}
max_data_points = 100  # Anzahl der Messungen, bevor das Diagramm aktualisiert wird

# Set up für den Webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Führe den Browser im Hintergrund aus
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Funktion zum Messen der Ladezeit
def measure_load_time(url):
    start_time = time.time()  # Startzeit messen
    try:
        driver.get(url)
        load_time = time.time() - start_time  # Ladezeit berechnen
        return load_time
    except Exception as e:
        print(f"Fehler beim Laden der Seite {url}: {e}")
        return None

# Funktion zum Aktualisieren des Diagramms
def update(frame):
    for url in urls:
        load_time = measure_load_time(url)
        if load_time is not None:
            load_times[url].append(load_time)
            if len(load_times[url]) > max_data_points:
                load_times[url].pop(0)  # Entfernt den ältesten Wert

    plt.cla()  # Löscht das Diagramm für ein frisches Zeichnen
    for url in urls:
        plt.plot(load_times[url], label=f"Ladezeit {url}")

        # Letzte Ladezeit und Durchschnitt berechnen
        last_time = load_times[url][-1]
        avg_time = sum(load_times[url]) / len(load_times[url])
        
        # Letzte Ladezeit und Durchschnittswert anzeigen
        plt.text(len(load_times[url])-1, last_time + 0.01, f"{last_time:.2f}s", ha='center', color='blue')
        plt.text(len(load_times[url])-1, avg_time + 0.01, f"Avg: {avg_time:.2f}s", ha='center', color='orange')
        plt.axhline(y=sum(load_times[url])/len(load_times[url]), color='y', linestyle='--', label="Durchschnitt")

    # Bestimme den besten und schlechtesten Wert
    all_load_times = [lt for times in load_times.values() for lt in times if lt is not None]
    if all_load_times:
        best_time = min(all_load_times)
        worst_time = max(all_load_times)
        plt.axhline(y=best_time, color='g', linestyle='--', label="Beste Ladezeit")
        plt.axhline(y=worst_time, color='r', linestyle='--', label="Schlechteste Ladezeit")
        

    plt.title("Ladezeiten mehrerer Websites")
    plt.xlabel("Anzahl der Messungen")
    plt.ylabel("Ladezeit (Sekunden)")
    plt.legend(loc="upper right")
    plt.tight_layout()

# Hauptprogramm zur Ausführung
if __name__ == "__main__":
    try:
        # Setup für das Diagramm
        fig = plt.figure()
        
        # Real-Time Plot mit Animation
        ani = FuncAnimation(fig, update, interval=1000)  # Aktualisierung alle 1 Sekunde
        
        plt.show()
    finally:
        driver.quit()  # Schließt den Webdriver am Ende
