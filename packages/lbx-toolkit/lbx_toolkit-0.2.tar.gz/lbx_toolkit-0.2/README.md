# Biblioteca de ferramentas LBX S/A

Esta biblioteca possui ferramentas comuns desenvolvidas originalmente para uso nos scripts da empresa LBX S/A

## Classe e funções

**Auth_MS365**:             Utiliza o seriço Microsoft(c) 365 para autenticar o usuário e previnir o uso não autorizado do script.
    _- valida_grupo():_     Autentica o usuário e checa se ele pertence a um grupo de segurança específico, abortando o script caso negativo
    _- disclaimer():_       Aviso sobre a necessidade de autenticação e parametros de execução/acesso
**PostgreSQL**:             Acessa e interage com o banco de dados PostgreSQL
    _- db():_               Inicia sessão com o banco
    _- csv_df():_           Le arquivo CSV e gera Dataframe do Pandas a partir dele
    _- db_insert_df():_     Insere informações de um Dataframe (Pandas) em uma tabela do banco com estrutura equivalente
    _- db_select():_        Retorna um cursor à partir e uma query
**API**:                    Interage com APIs RESTfull, especialmente providas para o ERP Sienge
    _- auth_base():_        Autentica (HTTPBasicAuth) sessão na API
    _- endpoint_json():_    Envia um payload em formato json para um Endpoint da API autenticada
    _- close():_            Encerra a sessão autenticada

## Instalação e uso:

### Instalação

```
pip install lbx_toolkit
```

### Uso
```
from lbx_toolkit import Auth_MS365, PostgreSQL, API ## liste a(s) classe(s) que deseja importar
```

Classe **Auth_M365**

Necessário obter as credencias de seu contrato Microsoft(c) 365, em específico client_id, client_secret e tenant_id
Sugerimos não armazenar informações sensíveis. Considere usar o pacote ```dotenv``` para isso

```
client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'
tenant_id = 'SEU_TENANT_ID'

auth = Auth_M365(client_id, client_secret, tenant_id, timeout=60, log_file='auth_office365_lbx.log')  ## timeout e log_file são opcionais e se omitidos, os valores aqui atribuídos serão adotados como padrão
auth.valida_grupo('Nome do Grupo de Distribuição') ## se usuário não pertencer a grupo informado, a execução do script é abortada.
```