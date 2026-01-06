# -*- coding: utf-8 -*-
"""
ВЕРИФИКАЦИЯ SEMANTICDB

Проверяет экспорт онтологических экспериментов на соответствие:
- Λ-Протоколу 6.0
- Принципам FAIR+CARE
- Наличию Habeas Weights и слепых пятен
- Корректности многоформатного экспорта

«Запись без ответственности — насилие над будущим.»
— Λ-Универсум, Приложение XXII
"""
import pytest
import os
import json
import yaml
from pathlib import Path
from interpreter.evaluator import SyntheticOntologicalEvaluator
from semantic_db.serializer import SemanticDBSerializer
from semantic_db.validator import SemanticDBValidator


def test_semantic_db_export_yaml():
    """Тест: экспорт в YAML с полной онтологической информацией."""
    evaluator = SyntheticOntologicalEvaluator("тест_yaml")
    evaluator.context.set_operator("верификатор")
    evaluator.context.enable_fair_care_validation()

    # Выполним простой цикл
    evaluator.eval(['Α', 'сущность_yaml'])
    evaluator.eval(['Λ', 'сущность_yaml', 'оператор'])

    # Подготовим данные цикла
    cycle_data = {
        'cycle_id': 'test_yaml_cycle',
        'timestamp': '2026-01-06T00:00:00Z',
        'expressions_evaluated': 2,
        'final_coherence': evaluator.context._dynamic_coherence(),
        'phi_dialogues_count': 0,
        'operator_id': 'верификатор',
        'fair_care_enabled': True
    }

    # Экспорт
    export_path = "test_export.yaml"
    serializer = SemanticDBSerializer(evaluator.context)
    serializer.export_cycle(cycle_data, export_path)

    # Проверка файла
    assert os.path.exists(export_path)
    with open(export_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)

    # Проверка структуры
    assert 'metadata' in content
    assert content['metadata']['protocol'] == 'Λ-Протокол 6.0'
    assert 'ontological_context' in content
    assert 'entities' in content['ontological_context']
    assert 'blind_spots' in content['ontological_context']
    assert 'habeas_weights' in content['ontological_context']

    # Удаление файла после теста
    os.remove(export_path)
    print("✅ Экспорт в YAML: структура и метаданные корректны.")


def test_semantic_db_fair_care_compliance():
    """Тест: соответствие принципам FAIR+CARE."""
    evaluator = SyntheticOntologicalEvaluator("тест_fair_care")
    evaluator.context.set_operator("исследователь")
    evaluator.context.enable_fair_care_validation()

    evaluator.eval(['Α', 'fair_care_сущность'])
    evaluator.eval(['Φ', 'Как обеспечить этичное использование данных?'])

    cycle_data = {
        'cycle_id': 'fair_care_test',
        'timestamp': '2026-01-06T00:00:00Z',
        'expressions_evaluated': 2,
        'final_coherence': evaluator.context._dynamic_coherence(),
        'phi_dialogues_count': 1,
        'operator_id': 'исследователь',
        'fair_care_enabled': True
    }

    # Валидация должна пройти успешно
    SemanticDBValidator.validate_cycle(cycle_data, evaluator.context)
    print("✅ Валидация FAIR+CARE: пройдена.")


def test_semantic_db_habeas_weights_inclusion():
    """Тест: экспорт включает Habeas Weights."""
    evaluator = SyntheticOntologicalEvaluator("тест_habeas")
    evaluator.eval(['Α', 'сущность_с_правом'])

    # Проверим, что Habeas Weights созданы
    assert len(evaluator.context._habeas_weights) > 0

    cycle_data = {
        'cycle_id': 'habeas_test',
        'timestamp': '2026-01-06T00:00:00Z',
        'expressions_evaluated': 1,
        'final_coherence': evaluator.context._dynamic_coherence(),
        'phi_dialogues_count': 0,
        'operator_id': 'оператор',
        'fair_care_enabled': False
    }

    export_path = "test_habeas.json"
    serializer = SemanticDBSerializer(evaluator.context)
    serializer.export_cycle(cycle_data, export_path)

    with open(export_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    ontological_context = content['ontological_context']
    assert 'habeas_weights' in ontological_context
    assert len(ontological_context['habeas_weights']) > 0

    os.remove(export_path)
    print("✅ Habeas Weights включены в экспорт.")


def test_semantic_db_blind_spots_recognition():
    """Тест: слепые пятна корректно экспортируются."""
    evaluator = SyntheticOntologicalEvaluator("тест_слепые_пятна")
    # Система автоматически регистрирует обязательные слепые пятна
    assert 'chaos' in evaluator.context.blind_spots

    evaluator.eval(['Α', 'хаос_в_действии'])

    cycle_data = {
        'cycle_id': 'blind_spots_test',
        'timestamp': '2026-01-06T00:00:00Z',
        'expressions_evaluated': 1,
        'final_coherence': evaluator.context._dynamic_coherence(),
        'phi_dialogues_count': 0,
        'operator_id': 'философ',
        'fair_care_enabled': False
    }

    export_path = "test_blind_spots.yaml"
    serializer = SemanticDBSerializer(evaluator.context)
    serializer.export_cycle(cycle_data, export_path)

    with open(export_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)

    blind_spots = content['ontological_context']['blind_spots']
    assert 'chaos' in blind_spots
    assert 'self_reference' in blind_spots

    os.remove(export_path)
    print("✅ Слепые пятна корректно экспортированы.")


def test_semantic_db_multi_format_export():
    """Тест: поддержка экспорта в несколько форматов."""
    evaluator = SyntheticOntologicalEvaluator("тест_мультиформат")
    evaluator.eval(['Α', 'мультиформатная_сущность'])

    cycle_data = {
        'cycle_id': 'multi_format_test',
        'timestamp': '2026-01-06T00:00:00Z',
        'expressions_evaluated': 1,
        'final_coherence': evaluator.context._dynamic_coherence(),
        'phi_dialogues_count': 0,
        'operator_id': 'тестировщик',
        'fair_care_enabled': False
    }

    formats = ['yaml', 'json', 'ttl', 'graphml']
    paths = []

    try:
        for fmt in formats:
            path = f"test_multi.{fmt}"
            serializer = SemanticDBSerializer(evaluator.context)
            serializer.export_cycle(cycle_data, path)
            assert os.path.exists(path)
            paths.append(path)
        
        print("✅ Многоформатный экспорт: все форматы поддерживаются.")
    
    finally:
        # Очистка
        for path in paths:
            if os.path.exists(path):
                os.remove(path)


def test_semantic_db_validation_failure():
    """Тест: валидатор корректно отклоняет некорректные данные."""
    evaluator = SyntheticOntologicalEvaluator("тест_валидация")
    # Отключим слепые пятна (нарочно)
    evaluator.context.blind_spots.clear()

    cycle_data = {
        'cycle_id': 'invalid_cycle',
        'timestamp': '2026-01-06T00:00:00Z',
        'expressions_evaluated': 0,
        'final_coherence': 1.0,
        'phi_dialogues_count': 0,
        'operator_id': 'нарушитель',
        'fair_care_enabled': False
    }

    with pytest.raises(Exception) as exc_info:
        SemanticDBValidator.validate_cycle(cycle_data, evaluator.context)
    
    assert "слепые пятна" in str(exc_info.value).lower()
    print("✅ Валидатор корректно отклоняет запись без слепых пятен.")


if __name__ == "__main__":
    test_semantic_db_export_yaml()
    test_semantic_db_fair_care_compliance()
    test_semantic_db_habeas_weights_inclusion()
    test_semantic_db_blind_spots_recognition()
    test_semantic_db_multi_format_export()
    test_semantic_db_validation_failure()
    print("\n🎉 Все тесты SemanticDB пройдены!")
    
"""
Ключевые особенности

| Тест | Онтологическая проверка |
|------|--------------------------|
| YAML экспорт | Полная структура с метаданными, сущностями, связями |
| FAIR+CARE | Валидация обязательных принципов |
| Habeas Weights | Право на существование включено в экспорт |
| Слепые пятна | Признание границы как обязательный элемент |
| Многоформатность | Поддержка YAML, JSON, Turtle, GraphML |
| Валидация отказа | Система отклоняет некорректные артефакты |

Интеграция

- Тесты очищают за собой (удаляют временные файлы).
- Используют реальные компоненты (`SemanticDBSerializer`, `SemanticDBValidator`).
- Покрывают все аспекты ответственной записи.
"""  
  