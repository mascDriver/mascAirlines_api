<p align="center">
    <img width="800" src="docs/_media/logo.png" title="Logo do projeto"><br />
    <img src="https://img.shields.io/maintenance/yes/2023?style=for-the-badge" title="Status do projeto">
    </p>

# MascAirlines (API)

Backend da companhia area MascAirlines onde é possível cadastrar usuarios, consultar preço de rotas e fazer compra.
> **IMPORTANTE:** Projeto ficticio
> 
## ✨ Features

Aqui você pode colocar uma screenshot do produto resultante desse projeto. Descreva também suas features usando uma lista:

* ✔️ Fácil integração;
* 🥢 Poucas dependências;
* 🖖 Possui ótima documentação e testes.

## 🚀 Começando

### 1. Primeiro passo para começar

Instale o poetry em sua maquina:
https://python-poetry.org/docs/

Se já estiver instalado, utilize:

```
poetry install
```
 Para executar o server, utilize:
```shell
poetry run uvicorn main:app --reload
```

### 2. Outro(s) passo(s)

Para alimentar a base de dados com cidades e estados, use esse codigo python:

```python
import httpx
from users.models import Uf, City
from db.database import SessionLocal
db = SessionLocal()
ufs = []
for uf in httpx.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados').json():
    ufs.append(Uf(id=uf['id'], abbreviation=uf['sigla'], name=uf['nome']))
db.add_all(ufs)
db.commit()

cidades = []
for cidade in httpx.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios').json():
    cidades.append(City(id=cidade['id'], uf_id=cidade['microrregiao']['mesorregiao']['UF']['id'], name=cidade['nome']))
db.add_all(cidades)
db.commit()

```
Para popular todo o banco use esse codigo
```python

from users.models import Consumer, City, User
from plane.models import Plane, Seat, Route
from db.database import SessionLocal
from faker import Faker
import random
db = SessionLocal()
fake = Faker(['pt_BR'])
citys = db.query(City).all()
for _ in range(100):
    user = User(name=fake.first_name(), last_name=fake.last_name(), email=fake.email(), password=fake.random_int(max=3))
    db.add(user)
    db.commit()
    consumer = Consumer(cellphone=fake.cellphone_number(), address=fake.address(), city_id=random.randint(0, 5570),
                        user_id=user.id)
    db.add(consumer)

for _ in range(50):
    plane = Plane(model=fake.random_letter(), tax_business=fake.random_int(max=3), tax_premium=fake.random_int(max=3))
    db.add(plane)
    db.commit()
    for __ in range(10):
        seat = Seat(plane_id=plane.id, is_business=True, is_economy=False)
        db.add(seat)
        db.commit()
    for __ in range(10):
        seat = Seat(plane_id=plane.id, is_premium=True, is_economy=False)
        db.add(seat)
        db.commit()
    for __ in range(60):
        seat = Seat(plane_id=plane.id)
        db.add(seat)
        db.commit()
    for __ in range(100):
        route = Route(plane_id=plane.id, origin_id=random.randint(0, 5570), destiny_id=random.randint(0, 5570),
                      price=fake.pricetag().replace('R$', '').replace('.', '').replace(',', '.'), depart=fake.future_datetime(), arrival=fake.future_datetime())
        db.add(route)
        db.commit()
        

```
### 3. DOC
Para verificar a doc do projeto acesse:

```http request
http://127.0.0.1:8000\docs
```
## 🤝 Contribua

Sua ajuda é muito bem-vinda, independente da forma! Confira o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para conhecer todas as formas de contribuir com o projeto. Por exemplo, [sugerir uma nova funcionalidade](https://github.com/ccuffs/template/issues/new?assignees=&labels=&template=feature_request.md&title=), [reportar um problema/bug](https://github.com/ccuffs/template/issues/new?assignees=&labels=bug&template=bug_report.md&title=), [enviar um pull request](https://github.com/ccuffs/hacktoberfest/blob/master/docs/tutorial-pull-request.md), ou simplemente utilizar o projeto e comentar sua experiência.

Veja o arquivo [ROADMAP.md](ROADMAP.md) para ter uma ideia de como o projeto deve evoluir.


## 🎫 Licença

Esse projeto é licenciado nos termos da licença open-source [MIT](https://choosealicense.com/licenses/mit) e está disponível de graça.

## 🧬 Changelog

Veja todas as alterações desse projeto no arquivo [CHANGELOG.md](CHANGELOG.md).
