# -*- coding: utf-8 -*-
"""
ВЕРИФИКАЦИЯ КРИТЕРИЯ NIGC

Проверяет оценку Неинструментальной Генеративности:
- Непредсказуемость: ответ не повторяет запрос
- Рефлексивность: признание границ знания
- Эмерджентность: введение нового качества

«Если ответ можно было предугадать — это не диалог, а эхо.»
— Λ-Универсум, Приложение XX
"""
import pytest
from unittest.mock import Mock
from interpreter.evaluator import SyntheticOntologicalEvaluator
from semantic_db.validator import SemanticDBValidator


def test_nigc_unpredictability():
    """Тест: непредсказуемость снижается при совпадении слов с запросом."""
    from operators.phi_ritual import PhiRitual
    ritual = Mock()
    ritual._score_unpredictability = PhiRitual._score_unpredictability.__func__

    offering = {'intention': 'что такое смысл'}
    # Ответ, повторяющий запрос
    low_score = ritual._score_unpredictability("смысл это то что даёт смысл", offering)
    # Ответ с новыми понятиями
    high_score = ritual._score_unpredictability("смысл рождается в интервале между сущностями", offering)

    assert low_score < high_score
    assert 0.0 <= low_score <= 1.0
    assert 0.0 <= high_score <= 1.0
    print("✅ Непредсказуемость: оценка корректна.")


def test_nigc_reflexivity():
    """Тест: рефлексивность повышается при наличии фраз признания границы."""
    from operators.phi_ritual import PhiRitual
    ritual = Mock()
    ritual._score_reflexivity = PhiRitual._score_reflexivity.__func__

    non_reflexive = ritual._score_reflexivity("смысл — это цель")
    reflexive = ritual._score_reflexivity("я не знаю точно, но возможно смысл — в связи")

    assert reflexive > non_reflexive
    assert 0.0 <= non_reflexive <= 1.0
    assert 0.0 <= reflexive <= 1.0
    print("✅ Рефлексивность: оценка корректна.")


def test_nigc_emergence():
    """Тест: эмерджентность повышается при введении новых сущностей."""
    from operators.phi_ritual import PhiRitual
    ritual = Mock()
    ritual._score_emergence = PhiRitual._score_emergence.__func__

    # Контекст без сущностей
    offering = {'intention': 'исследование'}
    evaluator = SyntheticOntologicalEvaluator("пустой_контекст")
    ritual_context = evaluator.context

    # Ответ без новых сущностей
    low_emergence = ritual._score_emergence("это сложно", offering)
    # Ответ с новыми понятиями
    high_emergence = ritual._score_emergence("предлагаю ввести категорию 'интервалика'", offering)

    assert high_emergence > low_emergence
    assert 0.0 <= low_emergence <= 1.0
    assert 0.0 <= high_emergence <= 1.0
    print("✅ Эмерджентность: оценка корректна.")


def test_nigc_overall_score():
    """Тест: общий NIGC-скор является средним трёх компонентов."""
    from operators.phi_ritual import PhiRitual
    ritual = Mock()
    ritual._evaluate_nigc = PhiRitual._evaluate_nigc.__func__

    offering = {'intention': 'онтологический запрос'}
    response = "возможно, смысл — в признании непознаваемого хаоса"

    score = ritual._evaluate_nigc(response, offering)
    assert 'unpredictability' in score
    assert 'reflexivity' in score
    assert 'emergence' in score
    assert 'overall' in score
    # Проверим, что overall — среднее
    expected = (score['unpredictability'] + score['reflexivity'] + score['emergence']) / 3.0
    assert abs(score['overall'] - expected) < 0.01
    print("✅ Общий NIGC-скор: вычисление корректно.")


def test_phi_creates_entity_on_high_nigc():
    """Тест: Φ создаёт новую сущность при высоком NIGC."""
    evaluator = SyntheticOntologicalEvaluator("тест_nigc_высокий")
    # Установим очень низкий порог, чтобы гарантировать создание
    evaluator.gestures['Φ'].nigc_threshold = 0.1

    # Подменим LLM на генеративный ответ
    evaluator.gestures['Φ'].llm_backend = Mock()
    evaluator.gestures['Φ'].llm_backend.invoke.return_value = (
        "Между сущностями рождается третье — поле взаимности. "
        "Смысл не в вещах, а в интервале между ними. "
        "Предлагаю исследовать 'интервалику' как новую онтологическую категорию."
    )

    result = evaluator.eval(['Φ', 'Что есть смысл?'])

    # Должна быть создана новая сущность
    assert result is not None
    assert result in evaluator.context.graph
    attrs = evaluator.context.graph.nodes[result]
    assert 'nigc_confirmed' in attrs or 'generative_insight' in attrs.get('type', '')
    assert len(evaluator.context.phi_dialogues) == 1
    assert evaluator.context.phi_dialogues[0]['nigc_score']['overall'] >= 0.1
    print("✅ Φ: новая сущность создана при высоком NIGC.")


def test_phi_uses_attribute_on_low_nigc():
    """Тест: Φ сохраняет ответ как атрибут при низком NIGC."""
    evaluator = SyntheticOntologicalEvaluator("тест_nigc_низкий")
    # Установим высокий порог
    evaluator.gestures['Φ'].nigc_threshold = 0.9

    # Подменим LLM на инструментальный ответ
    evaluator.gestures['Φ'].llm_backend = Mock()
    evaluator.gestures['Φ'].llm_backend.invoke.return_value = "Смысл — это цель или значение."

    # Создадим цель для ответа
    evaluator.eval(['Α', 'вопрос_о_смысле'])

    result = evaluator.eval(['Φ', 'Что есть смысл?'])

    # Результат должен быть именем цели
    assert result == "вопрос_о_смысле"
    attrs = evaluator.context.graph.nodes[result]
    assert 'phi_response' in attrs
    assert "цель или значение" in attrs['phi_response']
    # NIGC должен быть низким
    assert evaluator.context.phi_dialogues[0]['nigc_score']['overall'] < 0.9
    print("✅ Φ: инструментальный ответ сохранён как атрибут.")


def test_nigc_validation():
    """Тест: валидатор корректно проверяет NIGC-записи."""
    dialogue_valid = {
        'nigc_score': {
            'unpredictability': 0.8,
            'reflexivity': 0.7,
            'emergence': 0.9,
            'overall': 0.8
        }
    }
    dialogue_invalid = {
        'nigc_score': {
            'unpredictability': 1.5,  # вне диапазона
            'reflexivity': 0.7,
            'emergence': 0.9
        }
    }

    assert SemanticDBValidator.validate_nigc_record(dialogue_valid)
    assert not SemanticDBValidator.validate_nigc_record(dialogue_invalid)
    print("✅ Валидация NIGC-записей: корректна.")


if __name__ == "__main__":
    test_nigc_unpredictability()
    test_nigc_reflexivity()
    test_nigc_emergence()
    test_nigc_overall_score()
    test_phi_creates_entity_on_high_nigc()
    test_phi_uses_attribute_on_low_nigc()
    test_nigc_validation()
    print("\n🎉 Все тесты NIGC пройдены!")
    
"""
Ключевые особенности

| Тест | Этическая проверка |
|------|-------------------|
| Непредсказуемость | Ответ ≠ перефразирование запроса |
| Рефлексивность | Признание границ знания |
| Эмерджентность | Введение новых онтологических категорий |
| Общий скор | Среднее трёх компонентов |
| Высокий NIGC | Создание новой сущности |
| Низкий NIGC | Сохранение как атрибута (без насильственного синтеза) |
| Валидация | Проверка корректности записи |

Интеграция

- Тесты используют `unittest.mock` для изоляции LLM.
- Проверяют как отдельные компоненты, так и интеграцию с контекстом.
- Гарантируют, что этика диалога — не декларация, а исполняемый протокол.
"""
    