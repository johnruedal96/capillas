import subprocess
import sys

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

_analyzer: AnalyzerEngine | None = None
_anonymizer: AnonymizerEngine | None = None


def _ensure_spacy_model(model: str):
    try:
        import spacy
        spacy.load(model)
    except OSError:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model])


def _add_custom_recognizers(analyzer: AnalyzerEngine):
    cedula_pattern = Pattern(
        name="colombia_cedula",
        score=0.85,
        regex=r"\b\d{8,10}\b",
    )
    cedula_recognizer = PatternRecognizer(
        supported_entity="COLOMBIA_CEDULA",
        patterns=[cedula_pattern],
        context=["cedula", "cédula", "cc", "documento", "identificación", "identificacion", "número de cédula"],
    )

    phone_pattern = Pattern(
        name="colombia_phone",
        score=0.75,
        regex=r"\b\d{7,10}\b",
    )
    phone_recognizer = PatternRecognizer(
        supported_entity="PHONE_NUMBER",
        patterns=[phone_pattern],
        context=["teléfono", "telefono", "celular", "móvil", "movil", "whatsapp", "número", "numero", "contacto"],
    )

    analyzer.registry.add_recognizer(cedula_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)


def get_analyzer() -> AnalyzerEngine:
    global _analyzer
    if _analyzer is None:
        _ensure_spacy_model("es_core_news_sm")
        _ensure_spacy_model("en_core_web_sm")
        provider = NlpEngineProvider(nlp_configuration={
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "es", "model_name": "es_core_news_sm"},
                {"lang_code": "en", "model_name": "en_core_web_sm"},
            ],
        })
        _analyzer = AnalyzerEngine(
            nlp_engine=provider.create_engine(),
            supported_languages=["es", "en"],
        )
        _add_custom_recognizers(_analyzer)
    return _analyzer


def get_anonymizer() -> AnonymizerEngine:
    global _anonymizer
    if _anonymizer is None:
        _anonymizer = AnonymizerEngine()
    return _anonymizer


def anonymize_text(text: str) -> tuple[str, dict]:
    analyzer = get_analyzer()
    anonymizer = get_anonymizer()

    results = analyzer.analyze(text=text, language="es")

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={
            "DEFAULT": OperatorConfig("replace", {"new_value": "[DATOS PERSONALES ELIMINADOS]"}),
        },
    )

    return anonymized_result.text, {"entities_found": len(results), "original_length": len(text)}
