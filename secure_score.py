from cryptography.fernet import Fernet

class SecureScore:
    def __init__(self, key_file="key.key", score_file="score.enc"):
        self.key_file = key_file
        self.score_file = score_file
        self.key = self._load_or_generate_key()

    def _load_or_generate_key(self):
        """Lädt den Schlüssel oder generiert ihn, falls er nicht existiert."""
        try:
            with open(self.key_file, "rb") as file:
                return file.read()
        except FileNotFoundError:
            return self._generate_key()

    def _generate_key(self):
        """Generiert einen neuen Schlüssel und speichert ihn."""
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as file:
            file.write(key)
        return key

    def save_score(self, score):
        """Verschlüsselt und speichert den Score."""
        fernet = Fernet(self.key)
        encrypted_score = fernet.encrypt(str(score).encode())
        with open(self.score_file, "wb") as file:
            file.write(encrypted_score)

    def load_score(self):
        """Lädt und entschlüsselt den Score."""
        try:
            fernet = Fernet(self.key)
            with open(self.score_file, "rb") as file:
                encrypted_score = file.read()
            return int(fernet.decrypt(encrypted_score).decode())
        except (FileNotFoundError, ValueError):
            return 0  # Standardwert, falls keine Datei existiert oder fehlerhafte Daten vorliegen
