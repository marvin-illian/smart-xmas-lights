# main.py

from light_string_manager import LightStringManager

def main():
    """
    Hauptfunktion zur Initialisierung des LightStringManagers, Einschalten aller Lichter,
    Ausführen des Konvergenzeffekts und sauberen Beenden.
    """
    manager = LightStringManager()
    manager.turn_on_all()

    # Index of the light string to which the effects should converge (0-based index)
    target_index = 2

    try:
        print("Starte Licht-Programm...")
        # Konvergenzeffekt für eine bestimmte Dauer und Frames pro Sekunde ausführen
        manager.run_converging_effect(target_index=target_index, duration=10, fps=1)
    except KeyboardInterrupt:
        print("Unterbrechung durch Benutzer erkannt.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        print("Schalte alle Lichter aus.")
        manager.turn_off_all()

if __name__ == "__main__":
    main()