"""
Language-specific configuration for job scraping and filtering.
Contains language-specific keywords and filtering rules.
"""

class LanguageConfig:
    """Base class for language-specific configurations."""
    
    def __init__(self, code, name, required_keywords, student_keywords, country_search_location):
        self.code = code
        self.name = name
        self.required_keywords = required_keywords  # Keywords indicating advanced language requirements
        self.student_keywords = student_keywords    # Keywords for working student jobs
        self.country_search_location = country_search_location  # Country-wide search location
    
    def __repr__(self):
        return f"{self.name} ({self.code})"


class German(LanguageConfig):
    """German language configuration (DE)."""
    
    def __init__(self):
        required_keywords = [
            "C2 Deutsch",
            "C1 Deutsch",
            "Deutsch C2",
            "Deutsch C1",
            "Deutschkenntnisse auf C2-Niveau",
            "Deutschkenntnisse auf C1-Niveau",
            "German (C2)",
            "German (C1)",
            "Deutsch - Fließend",
            "verhandlungssicher Deutsch",
            "verhandlungssichere Deutschkenntnisse",
            "gute Deutschkenntnisse",
            "Sehr gute Deutsch",
            "fließend Deutsch",
            "Fließende Deutsch",
            "fluent in German",
            "Fluent German",
            "kommunizierst sicher auf Deutsch",
            "Deutschkenntnisse sind verhandlungssicher",
            "business fluent German",
            "Deutschkenntnisse auf Muttersprachenniveau",
            "Deutsch und Englisch verhandlungssicher in Wort und Schrift",
            "gute Deutsch",
            "Präsentationsfähigkeiten in Deutsch-",
            "Präsentationsfähigkeiten in Deutsch",
            "Beratungsfähigkeiten in Deutsch-",
            "Beratungsfähigkeiten in Deutsch",
            "Kommunikationsfähigkeiten in Deutsch",
            "Fluent in English and German",
            "mit Kunden / Kundenkontakt",
            "Präsentationen beim Kunden",
            "Stakeholder bis auf C-Level",
            "Excellent German",
            "Excellent English and German",
            "proficiency in German",
            "proficiency in English and German",
            "Very good English and German",
            "Kommunikationsfähigkeit in deutsche",
            "ausgezeichnete Deutsch",
            "kommunizierst sicher in Deutsch",
            "Fluent English and German",
            "Fluency in German",
            "Fluency in English and German",
            "excellent command of German"
        ]
        
        student_keywords = [
            "werkstudent",
            "intern",
            "thesis",
            "working student",
            "student assistant",
            "student worker",
            "praktikum",
            "hiwi",
            "abschlussarbeit",
            "internship",
            "werkstudenten"
        ]
        
        country_search_location = "Germany"
        
        super().__init__("DE", "German", required_keywords, student_keywords, country_search_location)


class Italian(LanguageConfig):
    """Italian language configuration (IT) - Framework for future expansion."""
    
    def __init__(self):
        required_keywords = [
            "C2 Italiano",
            "C1 Italiano",
            "italiano C2",
            "italiano C1",
            "fluent in Italian",
            "Fluent Italian",
            "excellent command of Italian",
            "ottima conoscenza dell'italiano",
            "madrelingua italiano"
        ]
        
        student_keywords = [
            "stage",
            "tirocinio",
            "apprendista",
            "tesi",
            "assistente studente",
            "studente lavoratore",
            "intern",
            "internship"
        ]
        
        country_search_location = "Italy"
        
        super().__init__("IT", "Italian", required_keywords, student_keywords, country_search_location)


# Registry of available language configurations
LANGUAGE_CONFIGS = {
    "DE": German,
    "IT": Italian
}

# Default language
DEFAULT_LANGUAGE = "DE"


def get_language_config(language_code):
    """Get a language configuration instance by code.
    
    Args:
        language_code: Language code (e.g., "DE", "IT")
        
    Returns:
        LanguageConfig instance
        
    Raises:
        ValueError: If language code is not found
    """
    if language_code not in LANGUAGE_CONFIGS:
        available = ", ".join(LANGUAGE_CONFIGS.keys())
        raise ValueError(f"Unknown language code '{language_code}'. Available: {available}")
    return LANGUAGE_CONFIGS[language_code]()
