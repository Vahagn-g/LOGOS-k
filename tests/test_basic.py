# -*- coding: utf-8 -*-
"""
БАЗОВАЯ ВЕРИФИКАЦИЯ LOGOS-κ

Проверяет фундаментальные компоненты:
- Лексер: извлечение φ-мета из ;;-комментариев
- Парсер: корректное построение AST
- Вычислитель: выполнение простых жестов
- Контекст: регистрация сущностей и связей

«Основа должна быть честной, иначе всё здание — иллюзия.»
— Λ-Универсум, Приложение V
"""
import pytest
from interpreter.lexer import OntologicalLexer
from interpreter.parser import OntologicalParser
from interpreter.evaluator import SyntheticOntologicalEvaluator
from core.axiom import OntologicalLimitError


def test_lexer_extracts_phi_meta():
    """Тест: лексер извлекает φ-мета из ;;-комментариев."""
    source = '''(Α "привет" ;; первое слово
                 :значение "коллапс потенции")'''
    lexer = OntologicalLexer(source)
    tokens = lexer.tokenize()
    phi_meta = lexer.get_phi_meta()

    assert tokens is not None
    assert len(tokens) > 0
    assert phi_meta == ["первое слово"]
    print("✅ Лексер корректно извлекает φ-мета.")


def test_parser_builds_ast():
    """Тест: парсер строит правильное AST."""
    source = '(Λ "A" "B" :через "внимание")'
    lexer = OntologicalLexer(source)
    tokens = lexer.tokenize()
    parser = OntologicalParser(tokens, lexer)
    ast = parser.parse()

    assert ast is not None
    assert len(ast) == 1
    expr = ast[0]
    assert expr[0] == 'Λ'
    assert expr[1] == 'A'
    assert expr[2] == 'B'
    assert expr[3] == ':через'
    assert expr[4] == 'внимание'
    print("✅ Парсер корректно строит AST.")


def test_evaluator_creates_entity():
    """Тест: вычислитель создаёт сущность через Α-жест."""
    evaluator = SyntheticOntologicalEvaluator("тест_контекст")
    result = evaluator.eval(['Α', 'тестовая_сущность'])

    assert result == "тестовая_сущность"
    assert "тестовая_сущность" in evaluator.context.graph
    node_data = evaluator.context.graph.nodes["тестовая_сущность"]
    assert node_data['type'] == 'entity'
    assert node_data['operator'] == 'Α'
    print("✅ Α-жест корректно создаёт сущность.")


def test_evaluator_creates_relation():
    """Тест: вычислитель создаёт связь через Λ-жест."""
    evaluator = SyntheticOntologicalEvaluator("тест_связь")
    # Сначала создадим сущности
    evaluator.eval(['Α', 'источник'])
    evaluator.eval(['Α', 'цель'])
    # Теперь связь
    result = evaluator.eval(['Λ', 'источник', 'цель'])

    assert result is not None
    assert evaluator.context.graph.has_edge('источник', 'цель')
    edge_data = evaluator.context.graph['источник']['цель']
    relation = edge_data.get('relation')
    assert relation is not None
    assert relation.type == 'Λ'
    assert relation.source == 'источник'
    assert relation.target == 'цель'
    print("✅ Λ-жест корректно создаёт связь.")


def test_context_tracks_coherence():
    """Тест: контекст вычисляет когерентность."""
    evaluator = SyntheticOntologicalEvaluator("тест_когерентность")
    # Создадим изолированную сущность
    evaluator.eval(['Α', 'одинокая_сущность'])
    coherence = evaluator.context._dynamic_coherence()

    # Когерентность должна быть снижена из-за изоляции
    assert 0.0 <= coherence < 1.0
    print(f"✅ Когерентность вычислена: {coherence:.2%}")


def test_axiom_limits_entities():
    """Тест: аксиома ограничивает число сущностей."""
    from core.axiom import OntologicalAxioms
    # Временно уменьшим лимит для теста
    original_limit = OntologicalAxioms.MAX_ENTITIES
    OntologicalAxioms.MAX_ENTITIES = 3

    try:
        evaluator = SyntheticOntologicalEvaluator("лимит_тест")
        for i in range(3):
            evaluator.eval(['Α', f'сущность_{i}'])
        
        # Четвёртая сущность должна вызвать ошибку
        with pytest.raises(OntologicalLimitError):
            evaluator.eval(['Α', 'сущность_3'])
        print("✅ Аксиома лимита сущностей работает.")
    
    finally:
        # Восстановим оригинальный лимит
        OntologicalAxioms.MAX_ENTITIES = original_limit


if __name__ == "__main__":
    # Позволяет запускать тесты напрямую
    test_lexer_extracts_phi_meta()
    test_parser_builds_ast()
    test_evaluator_creates_entity()
    test_evaluator_creates_relation()
    test_context_tracks_coherence()
    test_axiom_limits_entities()
    print("\n🎉 Все базовые тесты пройдены!")
    
"""
Ключевые особенности

| Тест | Онтологическая проверка |
|------|--------------------------|
| Лексер | Извлечение `φ-мета` — признание намерения оператора |
| Парсер | Корректное AST — основа для исполнения жестов |
| Α-жест | Создание сущности с правом на существование (Habeas Weights) |
| Λ-жест | Связь как активный агент (`OntologicalRelation`) |
| Когерентность | Измерение состояния онтологического пространства |
| Аксиомы | Работа предохранителей — условие устойчивости |

Интеграция

- Тесты совместимы с `pytest` (стандарт в Python).
- Можно запускать как модуль: `python -m pytest tests/test_basic.py -v`
- Или напрямую: `python tests/test_basic.py` (благодаря `if __name__ == "__main__"`).
"""   
