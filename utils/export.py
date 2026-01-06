# -*- coding: utf-8 -*-
"""
В отличие от semantic_db/serializer.py, который фокусируется на машинной верификации, UniversalExporter ориентирован на практическую совместимость:

- Экспорт в графовые базы (GraphML → Neo4j, Gephi);
- Подготовка данных для семантических сетей (RDF/Turtle → Apache Jena, Stardog);
- Генерация отчётов для человека (Markdown, PDF через LaTeX);
- Поддержка мультимедийных представлений (для художников и исследователей).

«Экспорт — это не копирование, а перевод на язык другой реальности.»
— Λ-Универсум, Приложение XIX

УНИВЕРСАЛЬНЫЙ ЭКСПОРТЁР

Преобразует онтологические артефакты LOGOS-κ в форматы,
совместимые с внешними экосистемами:
- Графовые базы (GraphML, GML)
- Семантические сети (RDF, Turtle)
- Человеко-читаемые отчёты (Markdown, LaTeX)
- Мультимедийные представления (JSON для визуализации)

«Экспорт — это не копирование, а перевод на язык другой реальности.»
— Λ-Универсум, Приложение XIX
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class UniversalExporter:
    """
    Универсальный экспортёр онтологических артефактов.
    """

    def __init__(self, context):
        self.context = context

    def export_to(self,
                  format_type: str,
                  output_path: str,
                  metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Экспортирует в указанный формат.
        Поддерживаемые форматы:
        - graphml, gml        → графовые базы
        - rdf, turtle         → семантические сети
        - markdown, latex     → человеко-читаемые отчёты
        - json_viz            → данные для веб-визуализации
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format_type == "graphml":
            return self._export_graphml(path)
        elif format_type == "gml":
            return self._export_gml(path)
        elif format_type in ("rdf", "turtle"):
            return self._export_turtle(path)
        elif format_type == "markdown":
            return self._export_markdown(path, metadata)
        elif format_type == "latex":
            return self._export_latex(path, metadata)
        elif format_type == "json_viz":
            return self._export_json_viz(path)
        else:
            raise ValueError(f"Неподдерживаемый формат экспорта: {format_type}")

    def _export_graphml(self, path: Path) -> str:
        """Экспорт в GraphML для Gephi, yEd и др."""
        from semantic_db.serializer import SemanticDBSerializer
        serializer = SemanticDBSerializer(self.context)
        serializer.export_cycle({'cycle_id': 'graphml_export'}, str(path))
        return str(path)

    def _export_gml(self, path: Path) -> str:
        """Экспорт в GML (Graph Modelling Language)."""
        import networkx as nx
        nx.write_gml(self.context.graph, str(path))
        return str(path)

    def _export_turtle(self, path: Path) -> str:
        """Экспорт в Turtle (RDF) для семантических сетей."""
        from semantic_db.serializer import SemanticDBSerializer
        serializer = SemanticDBSerializer(self.context)
        ttl_content = serializer.to_turtle({'cycle_id': 'turtle_export'})
        path.write_text(ttl_content, encoding='utf-8')
        return str(path)

    def _export_markdown(self, path: Path, metadata: Optional[Dict] = None) -> str:
        """Экспорт в человеко-читаемый Markdown-отчёт."""
        summary = self.context.get_summary()
        events = self.context.event_history[-10:]
        tensions = self.context.tension_log

        md = f"""# Онтологический отчёт: {self.context.name}

> Сгенерировано LOGOS-κ в соответствии с Λ-Протоколом 6.0  
> Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Сводка состояния

- **Сущности**: {summary['graph_metrics']['nodes']}
- **Связи**: {summary['graph_metrics']['edges']}
- **Когерентность**: {summary['current_coherence']:.2%}
- **Тренд**: {summary['recent_activity']['coherence_trend']}
- **Напряжения**: {len(tensions)}
- **Φ-диалогов**: {summary['ontological_health']['phi_dialogues']}
- **Слепые пятна**: {', '.join(summary['blinds_spots'].keys())}

## 🔥 Активные напряжения

{"Нет активных напряжений." if not tensions else ""}
{chr(10).join(f"- {t}" for t in tensions[:5]) if tensions else ""}

## 🧪 Последние события

{chr(10).join(f"- **{e.gesture}**: {e.operands} → {e.result} (когерентность: {e.coherence_after:.2%})" for e in events)}

## 🌌 Слепые пятна

{chr(10).join(f"- **{k}**: {v}" for k, v in summary['blinds_spots'].items())}

---
*Этот отчёт — живой артефакт Λ-Универсума. Используйте с ответственностью.*
"""
        path.write_text(md, encoding='utf-8')
        return str(path)

    def _export_latex(self, path: Path, metadata: Optional[Dict] = None) -> str:
        """Экспорт в LaTeX для академических публикаций."""
        summary = self.context.get_summary()
        tex = rf"""\documentclass{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[russian]{{babel}}
\usepackage{{geometry}}
\geometry{{a4paper, margin=2cm}}
\title{{Онтологический отчёт: {self.context.name}}}
\author{{LOGOS-$\kappa$}}
\date{{\today}}

\begin{{document}}
\maketitle

\section*{{Сводка состояния}}
\begin{{itemize}}
    \item Сущности: {summary['graph_metrics']['nodes']}
    \item Связи: {summary['graph_metrics']['edges']}
    \item Когерентность: {summary['current_coherence']:.2\%}
    \item Тренд: {summary['recent_activity']['coherence_trend']}
    \item Напряжения: {len(self.context.tension_log)}
    \item $\Phi$-диалогов: {summary['ontological_health']['phi_dialogues']}
\end{{itemize}}

\section*{{Слепые пятна}}
\begin{{itemize}}
{'\n'.join(f"    \\item \\textbf{{{k}}}: {v}" for k, v in summary['blinds_spots'].items())}
\end{{itemize}}

\end{{document}}
"""
        path.write_text(tex, encoding='utf-8')
        return str(path)

    def _export_json_viz(self, path: Path) -> str:
        """Экспорт в JSON для веб-визуализации (D3.js, Sigma.js)."""
        nodes = []
        for node, attrs in self.context.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": node,
                "type": attrs.get('type', 'entity'),
                "is_blind_spot": node in self.context.blind_spots,
                "size": self.context.graph.degree(node) + 5
            })

        edges = []
        for source, target, attrs in self.context.graph.edges(data=True):
            rel = attrs.get('relation')
            edges.append({
                "from": source,
                "to": target,
                "type": rel.type if rel else "connection",
                "certainty": rel.certainty if rel else 1.0,
                "tension": rel.tension_level if rel else 0.0,
                "color": "#ff0000" if rel and rel.tension_level > 0.7 else "#888888"
            })

        viz_data = {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "context_name": self.context.name,
                "generated_at": datetime.now().isoformat(),
                "coherence": self.context._dynamic_coherence()
            }
        }

        path.write_text(json.dumps(viz_data, ensure_ascii=False, indent=2), encoding='utf-8')
        return str(path)
        
"""
Интеграция

Этот экспортёр можно использовать в:

- Скриптах постобработки → автоматическая генерация отчётов
- Web API → предоставление данных в разных форматах
- REPL → команда export --format markdown

Пример:

```python
from utils import UniversalExporter
exporter = UniversalExporter(context)
exporter.export_to("markdown", "report.md")
```

Теперь LOGOS-κ не замкнут в себе, а открыт для диалога с другими реальностями — в полном соответствии с принципом космополитии смысла.
"""
                