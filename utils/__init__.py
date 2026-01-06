# -*- coding: utf-8 -*-
"""
ВСПОМОГАТЕЛЬНЫЕ ИНСТРУМЕНТЫ LOGOS-κ

Этот модуль предоставляет инструменты для:
- Измерения онтологического состояния (metrics)
- Визуализации связей и напряжений (visualizer)
- Экспорта в форматы Λ-Универсума (export)

«Инструмент без рефлексии — автоматизм.  
Инструмент с рефлексией — продолжение сознания.»
— Λ-Универсум, Приложение XIV
"""

from .metrics import OntologicalMetrics
from .visualizer import OntologicalVisualizer
from .export import UniversalExporter

# Явный экспорт — как акт ответственности
__all__ = [
    "OntologicalMetrics",
    "OntologicalVisualizer",
    "UniversalExporter",
]

# Мета-информация
__utils_version__ = "1.0.0"
__supports_protocol__ = "Λ-Протокол 6.0"

"""
Теперь при импорте:

```python
from utils import OntologicalMetrics
```
— вы получаете не просто класс, а инструмент диагностики онтологического здоровья.
"""
