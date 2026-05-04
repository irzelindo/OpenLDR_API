# OpenLDR_API — Plano de Refactor e Optimização

**Data:** 2026-04-23
**Autor:** Análise assistida
**Estado:** Proposta (diagnóstico, sem alterações de código)
**Escopo:** Todo o repositório (`auth/`, `configs/`, `db/`, `dict/`, `hiv/`, `tb/`, `utilities/`, `app.py`)

---

## 1. Sumário Executivo

A base de código do OpenLDR_API segue uma arquitectura MVC em camadas (routes → controllers → services → models) bem definida e consistente. O padrão é claro e a modularização entre domínios (TB GeneXpert, HIV VL, HIV EID, dict, auth) é sólida.

No entanto, existem **duplicações significativas** que aumentam o custo de manutenção e o risco de inconsistências:

- **~10 controllers** redefinem `_parse_common_args()` com pequenas variações.
- **~40+ métodos `get()`** repetem o mesmo boilerplate de extracção de JWT + tratamento de erros.
- **2 processadores de parâmetros** (`PROCESS_COMMON_PARAMS_FACILITY` e `PROCESS_COMMON_PARAMS_VL`) fazem trabalho sobreposto.
- **Listas de colunas de pacientes** (TB/VL) duplicadas em `utils.py` e nos respectivos serviços.
- **`utilities/utils.py`** acumulou 1542 linhas com responsabilidades heterogéneas.
- Uso intensivo de **`import *`** (8+ ficheiros) que obscurece dependências.

Este documento propõe um refactor **faseado**, priorizando mudanças de baixo risco (alto ROI, sem alteração de contratos de API) antes de mudanças estruturais maiores.

---

## 2. Inventário de Problemas

### 2.1 Duplicação de `_parse_common_args()` em controllers

**Ficheiros afectados (9):**

- `tb/gxpert/controllers/tb_gx_controller_facility.py`
- `tb/gxpert/controllers/tb_gx_controller_laboratory.py`
- `tb/gxpert/controllers/tb_gx_controller_patients.py`
- `tb/gxpert/controllers/tb_gx_controller_summary.py`
- `hiv/vl/controllers/vl_controller_facility.py`
- `hiv/vl/controllers/vl_controller_laboratory.py`
- `hiv/vl/controllers/vl_controller_patients.py`
- `hiv/vl/controllers/vl_controller_summary.py`
- `hiv/eid/controllers/eid_controller_laboratory.py` (variante `_parse_eid_common_args`)

Cada função define o mesmo conjunto base de argumentos (`interval_dates`, `province`, `district`, `health_facility`, `disaggregation`, `facility_type`), com sobreposições divergentes (`gene_xpert_result_type`, `type_of_laboratory`, `lab_type`, `result_type`, `test_reason`, `page`, `per_page`, etc.).

**Problema:** adicionar um novo parâmetro comum exige editar 9 ficheiros; esquecer 1 cria bugs silenciosos.

### 2.2 Boilerplate de JWT + try/except em cada endpoint

Padrão repetido em praticamente todos os métodos `get()`:

```python
token = get_token(request) or "Unknown"
try:
    token_payload = get_unverified_payload(token)
except Exception as e:
    return jsonify({"status": "error", "code": 500, ...})
session["user_info"] = get_user_token_info(token_payload)
user_id = str(session.get("user_info").get("user_id"))
req_args = _parse_common_args()
req_args["user_id"] = user_id
try:
    response = service(req_args)
    return jsonify(response)
except Exception as e:
    return jsonify({"error": "...", "status": 500})
```

O controller EID já extraiu parcialmente este padrão em `_execute_eid_service()` (ver `hiv/eid/controllers/eid_controller_laboratory.py:34-70`) — é a base a generalizar.

**Incoerências detectadas:**
- Mensagens variam entre `"An Error Occured"` (typo), `"An Error Occurred"`, `"An internal error occurred."`.
- Chave do código HTTP alterna entre `"code"` e `"status"`.
- Alguns retornam tuplo `(jsonify(...), 500)`, outros só `jsonify(...)`.

### 2.3 Dois processadores de parâmetros divergentes

- `utilities/utils.py:951` — `PROCESS_COMMON_PARAMS_FACILITY(args)` → tuple de **7 campos**
- `utilities/utils.py:1497` — `PROCESS_COMMON_PARAMS_VL(req_args)` → tuple de **5 campos**

Lógica central (normalização de `dates`, `disaggregation`, `facility_type`, `facilities`) é igual mas implementada duas vezes, com regras de inferência ligeiramente diferentes para `facility_type`. Referência adicional em `CLAUDE.md:294` menciona ainda `PROCESS_COMMON_PARAMS_LABORATORY()` (que não existe na árvore actual).

### 2.4 Listas de `with_entities` replicadas

Colunas do modelo `TBMaster` (33 colunas) definidas em:
- `utilities/utils.py:1087-1121` (função `get_patients`, ramo `tb`)
- `tb/gxpert/services/tb_gx_services_patients.py:101-134` (inline em `get_patients_by_name_service`)

Colunas do modelo `VlData` (~29 colunas) definidas em:
- `utilities/utils.py:1125-1156` (função `get_patients`, ramo `vl`)
- `hiv/vl/services/vl_services_patients.py:64-94` (constante `VL_PATIENT_ENTITIES`)

**Problema:** qualquer nova coluna exige edição em ≥ 2 sítios.

### 2.5 `utilities/utils.py` monolítico

1542 linhas, responsabilidades misturadas:
- Helpers de data SQL (`YEAR`, `MONTH`, `DAY`, `QUARTER`, `WEEK`, `DATE_PART`)
- Agregações (`TOTAL_ALL`, `TOTAL_NOT_NULL`, `TOTAL_NULL`, `TOTAL_IN`)
- Diferenças de data (`DATE_DIFF_AVG/MIN/MAX`)
- Helpers condicionais (`SUPPRESSION`, `GENDER_SUPPRESSION`, `LAB_TYPE`)
- Helpers de JWT (`get_token`, `get_unverified_payload`, `get_user_token_info`)
- Processadores de parâmetros (`PROCESS_COMMON_PARAMS_*`)
- Paginação + processamento de pacientes (`paginate_query`, `process_patients`, `get_patients`)
- Constantes temporais (`today`, `twelve_months_ago`) calculadas no import (ver 2.8)

### 2.6 `import *` generalizado

Usado em 8+ ficheiros (`from configs.paths import *`, `from utilities.utils import *`, `from tb.gxpert.services.tb_gx_services_patients import *`). Efeitos:

- Polui o namespace global dos módulos cliente.
- Torna imprevisível saber onde um símbolo é definido.
- Quebra o reload incremental de ferramentas de análise estática.
- Permite colisões silenciosas (p.ex. se `utils.py` e `paths.py` exportarem o mesmo nome).

### 2.7 `app.py` sem factory pattern

Configuração executada no momento do import do módulo:
- `db.init_app(app)` e `jwt = JWTManager(app)` no nível global.
- Rotas registadas no import.

Impede testes isolados (não é possível criar múltiplas instâncias `app` com configurações diferentes) e cria dependências circulares potenciais.

### 2.8 Constantes temporais estáticas

`utilities/utils.py:10-16`:
```python
getdate = datetime.now()
today = getdate.strftime("%Y-%m-%d")
twelve_months_ago = (getdate - relativedelta(months=12)).strftime(...)
```

Calculadas **uma vez** quando o módulo é importado. Num servidor que corra dias/semanas, `today` fica desactualizado → defaults de `interval_dates` tornam-se progressivamente incorrectos.

### 2.9 Ficheiros órfãos e inconsistências menores

- `__init_.py` na raiz (note o underscore duplo em falta — provável typo, mantém-se ficheiro vazio sem uso claro).
- Pastas placeholder: `hiv/ad/`, `tb/cultura/`, `hiv/dpi/` (mencionadas em CLAUDE.md) — confirmar se são realmente necessárias no repositório ou removíveis até serem implementadas.
- Typo persistente `"An Error Occured"` (sem duplo "r") em mensagens de erro.
- `configs/configs.zip` versionado — artefacto possivelmente acidental.
- Comentários TODO stale: `# from configs.paths_local import *` em múltiplos ficheiros.

### 2.10 Inconsistências de nomenclatura de classes de Resource

Convenções PascalCase vs snake_case conviveem:
- TB gxpert usa snake_case: `tb_gx_patients_by_name_controller`, `dashboard_header_component_summary_controller`.
- HIV VL/EID usa PascalCase: `VlPatientsByName`, `EidTestedSamplesByMonth`.

`CLAUDE.md:183` documenta PascalCase como padrão oficial. Os controllers TB violam a convenção.

### 2.11 Tratamento de role/admin replicado

Padrão `if user_role != "Admin": return 403` aparece em vários serviços (`tb_gx_services_patients.py`, `vl_services_patients.py`, etc.). Em VL já foi extraído para `_check_admin_access`; noutros módulos mantém-se inline.

---

## 3. Plano de Refactor (Faseado)

### Fase 1 — Extracções de baixo risco (sem mudança de contrato de API)

**Objectivo:** eliminar as duplicações mais evidentes. Zero alteração no comportamento externo.

#### 1.1 Criar `utilities/controller_helpers.py`

Conteúdo proposto:

```python
# utilities/controller_helpers.py
from functools import wraps
from flask import jsonify, request, session
from flask_restful import reqparse
from .utils import get_token, get_unverified_payload, get_user_token_info

# -- Parser builders -------------------------------------------------
_LIST_ARG = dict(type=lambda x: x, location="args", action="append")

def build_common_parser(*, extra_args=None):
    """
    Cria um reqparse.RequestParser com os argumentos comuns a todos os
    endpoints de reporting. `extra_args` é uma lista de tuplos
    (name, kwargs) para argumentos específicos do endpoint.
    """
    parser = reqparse.RequestParser()
    parser.add_argument("interval_dates", **_LIST_ARG)
    parser.add_argument("province", **_LIST_ARG)
    parser.add_argument("district", **_LIST_ARG)
    parser.add_argument("health_facility", type=str, location="args")
    parser.add_argument("facility_type", type=str, location="args")
    parser.add_argument("disaggregation", type=str, location="args")
    for name, kwargs in (extra_args or []):
        parser.add_argument(name, **kwargs)
    return parser


# -- Decorator para JWT + erros --------------------------------------
def _error_response(exc, message="An error occurred"):
    return jsonify({
        "status": "error",
        "code": 500,
        "message": message,
        "error": str(exc),
    }), 500


def with_auth_and_errors(parse_fn, service_fn):
    """
    Executa o pipeline:
      1. Valida JWT e popula sessão.
      2. Invoca parse_fn() para obter req_args.
      3. Injecta user_id.
      4. Chama service_fn(req_args) e devolve JSON.
      5. Normaliza qualquer erro em 500.
    """
    token = get_token(request) or "Unknown"
    try:
        payload = get_unverified_payload(token)
    except Exception as e:
        return _error_response(e, "Invalid or missing token")

    session["user_info"] = get_user_token_info(payload)
    user_id = str(session["user_info"].get("user_id"))

    try:
        req_args = parse_fn()
        req_args["user_id"] = user_id
        return jsonify(service_fn(req_args))
    except Exception as e:
        return _error_response(e)
```

**Migração dos controllers:** cada controller passa a:

```python
_parser = build_common_parser(extra_args=[
    ("gene_xpert_result_type", dict(type=str, location="args")),
    ("type_of_laboratory", dict(type=str, location="args")),
])

class tb_gx_registered_samples_by_lab_controller(Resource):
    def get(self):
        """... swagger ..."""
        return with_auth_and_errors(_parser.parse_args,
                                    registered_samples_by_lab_service)
```

**Impacto estimado:** redução ~400 linhas, 9 ficheiros de controller.

#### 1.2 Unificar `_check_admin_access` em `utilities/auth_helpers.py`

Mover de `hiv/vl/services/vl_services_patients.py` para local partilhado; substituir lógica inline em `tb/gxpert/services/tb_gx_services_patients.py` (linhas 53-72).

#### 1.3 Corrigir typos e padronizar mensagens de erro

- `"An Error Occured"` → `"An error occurred"` (todos os sítios).
- Usar sempre `"code"` (não `"status"`) para o código HTTP no payload.
- Retornar sempre tuple `(jsonify(...), http_status)` — mais idiomático em Flask-RESTful.

#### 1.4 Transformar constantes temporais estáticas em funções

```python
# utilities/utils.py
def today():
    return datetime.now().strftime("%Y-%m-%d")

def twelve_months_ago():
    return (datetime.now() - relativedelta(months=12)).strftime("%Y-%m-%d")
```

Actualizar os 2 sítios em `PROCESS_COMMON_PARAMS_*` para chamar as funções.

---

### Fase 2 — Unificação de modelos/entidades

#### 2.1 Centralizar entity lists em `<module>/models/entities.py`

```python
# tb/gxpert/models/entities.py
from .tb_gx_model import TBMaster

TB_PATIENT_ENTITIES = (
    TBMaster.RequestID,
    TBMaster.RequestingProvinceName,
    ...
)
```

```python
# hiv/vl/models/entities.py
from .vl import VlData

VL_PATIENT_ENTITIES = (
    VlData.RequestID,
    ...
)
```

Remover as duplicatas de `utils.py::get_patients` e do serviço VL. `get_patients` passa a receber `entities` como parâmetro, ou é movida para cada módulo.

#### 2.2 Consolidar `PROCESS_COMMON_PARAMS_FACILITY` e `PROCESS_COMMON_PARAMS_VL`

Criar uma função única `process_common_params(req_args, *, module: str)` que devolve um dataclass/NamedTuple:

```python
from dataclasses import dataclass

@dataclass
class CommonParams:
    dates: tuple[str, str]
    facilities: list[str]
    facility_type: str
    disaggregation: bool
    health_facility: str | None
    type_of_laboratory: str | None = None
    gx_result_type: str | None = None
    lab_type: str | None = None
```

Vantagens: acesso por nome em vez de desempacotamento posicional frágil; fim do risco de trocar posições ao adicionar campos.

Migração incremental: manter as funções antigas como wrappers que delegam para a nova durante período de transição.

---

### Fase 3 — Reorganização de `utilities/utils.py`

Dividir em submódulos:

```
utilities/
├── __init__.py          # re-exporta para backward compat (opcional)
├── sql.py               # YEAR, MONTH, DAY, QUARTER, DATE_PART, TOTAL_*, etc.
├── dates.py             # today(), twelve_months_ago(), DATE_DIFF_*
├── auth.py              # get_token, get_unverified_payload, get_user_token_info, _check_admin_access
├── params.py            # process_common_params + CommonParams
├── patients.py          # paginate_query, process_patients, get_patients (genérico)
├── controller_helpers.py (novo da Fase 1)
└── swagger.py           # mantém-se
```

Eliminar gradualmente os `from utilities.utils import *`.

---

### Fase 4 — App Factory

Refactorar `app.py`:

```python
def create_app(config_name="production"):
    app = Flask(__name__)
    _apply_config(app, config_name)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    JWTManager(app)
    Swagger(app, template=swagger_template)
    db.init_app(app)
    api = Api(app)
    _register_routes(api)
    _register_error_handlers(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
```

Permite criar instâncias para testes (`create_app("testing")`) e centraliza configuração.

---

### Fase 5 — Convenções e limpeza

- Renomear classes de controller TB para PascalCase conforme `CLAUDE.md:183` (requer actualização das rotas — breaking para quem importar directamente).
- Remover `__init_.py` da raiz se não for usado.
- Remover `configs/configs.zip` e adicioná-lo ao `.gitignore`.
- Remover comentários `# from configs.paths_local import *` (substituir por mecanismo de env var para alternar).
- Adicionar error handler global Flask (`@app.errorhandler(Exception)`) para garantir formato uniforme de erros 500.

---

## 4. Resumo de Impacto e Risco

| Fase | Descrição | LOC removidas (est.) | Risco | Dependências |
|------|-----------|----------------------|-------|--------------|
| 1    | Controller helpers + auth helpers + typos | ~400 | Baixo | Nenhuma |
| 2    | Unificar entity lists + params | ~200 | Médio | Fase 1 (opcional) |
| 3    | Split de `utils.py` | 0 (reorganização) | Médio | Fase 1, 2 |
| 4    | App factory | ~30 | Médio-Alto | Fase 1 |
| 5    | Convenções, limpeza | ~100 | Alto* | Fase 1-4 |

\* Fase 5 contém renomeações que podem quebrar imports externos à base de código (p.ex. scripts de deploy). Validar antes.

---

## 5. Validação Proposta

Como não existe suite de testes actualmente, sugerir antes do refactor:

1. **Smoke tests mínimos** — script que percorre cada endpoint Swagger (`/apidocs/`) com parâmetros default e compara payload antes/depois (snapshot testing).
2. **Fixar respostas de referência** — capturar 1 resposta por endpoint com um conjunto de parâmetros fixos; usar para regressão.
3. **Logging temporário** — adicionar middleware que loga `request.path + request.args` para uma amostra de tráfego real durante 1 semana, garantindo cobertura dos padrões usados em produção.

---

## 6. Ordem de Execução Recomendada

1. Fase 1.3 (typos) — PR isolada, trivial.
2. Fase 1.1 + 1.2 — PR única, reduz a maior fonte de duplicação.
3. Fase 1.4 (datas dinâmicas) — PR isolada, corrige bug latente.
4. Fase 2 — pode ser dividida em 2 PRs (entities, params).
5. Fase 3 — uma PR por submódulo extraído.
6. Fase 4 — PR independente, requer validação manual cuidadosa de arranque.
7. Fase 5 — várias PRs pequenas; deixar renomeações para último.

---

## 7. Itens NÃO abordados neste plano

- **Performance SQL** — não foi feita análise de queries; pode haver ganhos (índices, eager loading, query caching) que justifiquem plano separado.
- **Testes unitários** — ausência total; plano de cobertura deve ser tratado em spec dedicada.
- **Segurança** — revisar uso de `get_unverified_payload` (não valida assinatura do JWT?), política de CORS `"origins": "*"`, secret key default.
- **Observabilidade** — ausência de logging estruturado e métricas.
