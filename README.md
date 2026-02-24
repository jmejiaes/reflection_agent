# Reflection Agent

Agente LangGraph con loop **generar → reflexión → generar**. Pensado para organizar el código de forma clara para **LLMOps** (config por env, prompts separados, grafo y nodos modularizados).

## Estructura (LLMOps)

```
reflection_agent/
├── config/           # Configuración (modelo, env, límites)
│   ├── __init__.py
│   └── settings.py
├── graph/            # Grafo LangGraph
│   ├── __init__.py
│   ├── state.py      # Estado y constantes de nodos
│   ├── prompts.py    # Prompts (fácil versionado / A/B)
│   ├── chains.py     # Cadenas LCEL (prompt | llm)
│   ├── nodes.py      # Nodos del grafo
│   └── graph.py      # Construcción del grafo
├── examples/         # Ejemplos y experimentos
├── main.py           # Entrada: compila grafo y opcionalmente invoca
├── .env.example      # Variables de entorno de referencia
└── pyproject.toml
```

- **Config**: modelo, temperatura y `REFLECTION_MAX_MESSAGES` vía env (sin tocar código).
- **Prompts**: en `graph/prompts.py` para cambiar o versionar textos en un solo sitio.
- **Grafo**: definición en `graph/graph.py`; nodos en `graph/nodes.py`; estado en `graph/state.py`.

## Uso

```bash
cp .env.example .env   # Añade tu OPENAI_API_KEY
uv run python main.py  # o: python main.py
```

Variables opcionales en `.env`: `OPENAI_MODEL`, `OPENAI_TEMPERATURE`, `REFLECTION_MAX_MESSAGES`.

## Ejecutar desde la raíz

Los imports usan `config` y `graph`; ejecuta siempre desde la raíz del repo:

```bash
cd reflection_agent && python main.py
```
