import csv
import time
import os


class NetworkLogger:
    """
    Logger pour événements réseau (paquets envoyés, reçus, perdus).
    Stocke en mémoire puis exporte en CSV.
    """

    def __init__(self, file="network_log.csv"):
        self.file = file
        self.logs = []

    def log_packet(self, packet, status):
        """
        Enregistre un événement de paquet.
        status : sent | delivered | dropped | queued
        """

        if packet is None:
            return

        if not hasattr(packet, "source") or not hasattr(packet, "destination"):
            raise ValueError("Objet packet invalide")

        entry = {
            "timestamp": round(time.time(), 4),
            "source": packet.source.id,
            "destination": packet.destination.id,
            "size": packet.size,
            "status": status
        }

        self.logs.append(entry)

    def log_event(self, message):
        """
        Permet de logger un événement système (debug réseau)
        """
        self.logs.append({
            "timestamp": round(time.time(), 4),
            "source": "SYSTEM",
            "destination": "-",
            "size": 0,
            "status": message
        })

    def export_csv(self):
        """
        Exporte tous les logs dans un fichier CSV propre.
        """

        if not self.logs:
            return

        file_exists = os.path.isfile(self.file)

        with open(self.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["timestamp", "source", "destination", "size", "status"]
            )

            writer.writeheader()
            writer.writerows(self.logs)

    def clear(self):
        """
        Vide les logs en mémoire
        """
        self.logs.clear()

    def __repr__(self):
        return f"NetworkLogger({len(self.logs)} logs)"