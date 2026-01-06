# -*- coding: utf-8 -*-
"""
ИСПОЛНЯЕМЫЙ СЛОЙ LOGOS-κ

Этот модуль реализует интерфейс между онтологическим ядром и оператором:
- Лексер: извлечение φ-намерений из ;;-комментариев
- Парсер: построение AST из S-выражений
- Вычислитель: исполнение Λ-жестов в активном контексте
- REPL: интерактивный диалог с онтологическим пространством

«Исполнение — это не вычисление, а онтологическая трансформация.»
— Λ-Универсум, Приложение VIII
"""

# Явный экспорт ключевых компонентов
from .lexer import OntologicalLexer
from .parser import OntologicalParser
from .evaluator import SyntheticOntologicalEvaluator
from .repl import EnhancedLOGOSREPL

__all__ = [
    "OntologicalLexer",
    "OntologicalParser",
    "SyntheticOntologicalEvaluator",
    "EnhancedLOGOSREPL",
]

# Онтологические метаданные
__interpreter_version__ = "1.0.0"
__execution_model__ = "ritualistic"  # не "imperative", не "functional"