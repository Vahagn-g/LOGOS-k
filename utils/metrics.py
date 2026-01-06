# -*- coding: utf-8 -*-
"""
Согласно Λ-Универсуму, «когерентность — не истина, а условие состоятельности». Поэтому метрики здесь — не просто «аналитика», а диагностические признаки онтологического здоровья, помогающие оператору:

- Оценивать когерентность (согласованность связей),
- Отслеживать напряжения (противоречия, циклы, конфликты),
- Измерять активность Φ-диалогов,
- Выявлять деградацию (изоляция, фрагментация),
- Принимать решение о Ω-возврате или ∇-обогащении.

ОНТОЛОГИЧЕСКИЕ МЕТРИКИ

Измеряет здоровье онтологического пространства:
- Когерентность (согласованность связей)
- Напряжение (противоречия, циклы)
- Активность (создание сущностей, Φ-диалоги)
- Стабильность (тренды во времени)

«Когерентность — не истина, а условие состоятельности.»
— Λ-Универсум, Приложение VII
"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import networkx as nx


class OntologicalMetrics:
    """
    Инструмент для измерения онтологического состояния.
    """

    def __init__(self, context):
        self.context = context

    def get_comprehensive_health(self) -> Dict[str, Any]:
        """Возвращает полный отчёт о состоянии онтологического пространства."""
        coherence = self._compute_coherence()
        tension = self._compute_tension()
        activity = self._compute_activity()
        stability = self._compute_stability()

        return {
            'timestamp': datetime.now().isoformat(),
            'coherence': coherence,
            'tension': tension,
            'activity': activity,
            'stability': stability,
            'diagnosis': self._generate_diagnosis(coherence, tension, activity, stability),
            'recommendations': self._generate_recommendations(coherence, tension)
        }

    def _compute_coherence(self) -> Dict[str, float]:
        """Вычисляет когерентность как меру связности и согласованности."""
        graph = self.context.graph
        if graph.number_of_nodes() == 0:
            return {'value': 1.0, 'isolated_penalty': 0.0, 'fragmentation': 0.0}

        # Штраф за изолированные узлы
        isolated = sum(1 for n in graph.nodes() if graph.degree(n) == 0)
        isolated_penalty = isolated / graph.number_of_nodes()

        # Фрагментация: количество компонент связности
        components = nx.number_weakly_connected_components(graph)
        fragmentation = (components - 1) / max(1, graph.number_of_nodes())

        # Основная когерентность
        base = 1.0 - (isolated_penalty + fragmentation)
        value = max(0.0, min(1.0, base))

        return {
            'value': value,
            'isolated_penalty': isolated_penalty,
            'fragmentation': fragmentation,
            'isolated_nodes': isolated,
            'components': components
        }

    def _compute_tension(self) -> Dict[str, int]:
        """Вычисляет онтологическое напряжение."""
        # Напряжения из лога (противоречия, циклы)
        explicit_tensions = len(self.context.tension_log)

        # Циклы в графе (потенциально напряжённые)
        try:
            cycles = list(nx.simple_cycles(nx.DiGraph(self.context.graph)))
            cycle_tension = len(cycles)
        except Exception:
            cycle_tension = 0

        # Связи с высоким уровнем напряжения
        high_tension_relations = 0
        for _, _, attrs in self.context.graph.edges(data=True):
            rel = attrs.get('relation')
            if rel and hasattr(rel, 'tension_level') and rel.tension_level > 0.7:
                high_tension_relations += 1

        total = explicit_tensions + cycle_tension + high_tension_relations

        return {
            'total': total,
            'explicit': explicit_tensions,
            'cycles': cycle_tension,
            'high_tension_relations': high_tension_relations
        }

    def _compute_activity(self) -> Dict[str, int]:
        """Вычисляет уровень активности."""
        entities = self.context.graph.number_of_nodes()
        relations = self.context.graph.number_of_edges()
        phi_dialogues = len(self.context.phi_dialogues)
        events = len(self.context.event_history)

        # Темп событий за последние 5 минут (упрощённо)
        recent_events = 0
        now = datetime.now()
        for event in self.context.event_history[-20:]:  # последние 20 событий
            # Предполагаем, что event.timestamp — datetime
            if hasattr(event, 'timestamp') and (now - event.timestamp) < timedelta(minutes=5):
                recent_events += 1

        return {
            'entities': entities,
            'relations': relations,
            'phi_dialogues': phi_dialogues,
            'events': events,
            'recent_events_5min': recent_events
        }

    def _compute_stability(self) -> Dict[str, str]:
        """Оценивает стабильность на основе истории когерентности."""
        history = self.context._coherence_history
        if len(history) < 2:
            return {'trend': 'стабильность', 'volatility': 0.0}

        # Берём последние 10 точек
        recent = [coh for _, coh in history[-10:]]
        if len(recent) < 2:
            trend = 'стабильность'
        else:
            diff = recent[-1] - recent[0]
            if diff > 0.05:
                trend = 'улучшение'
            elif diff < -0.05:
                trend = 'ухудшение'
            else:
                trend = 'стабильность'

        # Волатильность = std отклонение
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        volatility = variance ** 0.5

        return {
            'trend': trend,
            'volatility': round(volatility, 3)
        }

    def _generate_diagnosis(self, coherence, tension, activity, stability) -> str:
        """Генерирует диагностическое заключение."""
        coh_val = coherence['value']
        tension_val = tension['total']
        trend = stability['trend']

        if coh_val < 0.3 and tension_val > 5:
            return "КРИЗИС: коллапс когерентности, высокое напряжение"
        elif coh_val < 0.5:
            return "ДЕГРАДАЦИЯ: фрагментация онтологического пространства"
        elif tension_val > 3 and trend == "ухудшение":
            return "НАРАСТАЮЩЕЕ НАПРЯЖЕНИЕ: риск онтологического конфликта"
        elif activity['recent_events_5min'] == 0 and coh_val > 0.8:
            return "СТАГНАЦИЯ: пространство стабильно, но не эволюционирует"
        else:
            return "ЗДОРОВОЕ СОСТОЯНИЕ: баланс между связью и напряжением"

    def _generate_recommendations(self, coherence, tension) -> List[str]:
        """Генерирует рекомендации на основе состояния."""
        recommendations = []
        coh_val = coherence['value']
        tension_val = tension['total']

        if coh_val < 0.4:
            recommendations.append("Рассмотрите Ω-возврат для извлечения инварианта")
        if tension_val > 3:
            recommendations.append("Инициируйте Φ-диалог для разрешения напряжений")
        if coherence['isolated_nodes'] > 5:
            recommendations.append("Создайте связи (Λ) для изолированных сущностей")
        if tension['cycles'] > 2:
            recommendations.append("Проверьте циклические зависимости на логичность")

        return recommendations if recommendations else ["Продолжайте наблюдение"]