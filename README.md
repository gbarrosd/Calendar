<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=%20CONCLUIDO&color=GREEN&style=for-the-badge"/>
<img src="https://img.shields.io/badge/Django-REST%20FRAMEWORK-green"/>
</p>
<hr>

# WeedWay Calender

O objetivo do projeto é construir uma API para simular a funcionalidade do [Calendly](https://calendly.com/).

## :hammer: Instalação e configuracao do projeto

- `1º passo`: Clone o repostorio na sua maquina.

- `2º passo`: Suba o docker ele vai instalar as dependencias necessarias do django assim como o banco

```bash
  docker compose up
```
- `3º passo`: Entre no container web
```bash
  docker exec -it teste-backend-web-1 bash
```
- `4º passo`: No terminal crie um Superusuário -> "python3 manage.py createsuperuser"
```bash
  python manage.py createsuperuser
```
- `5º passo`: Acesse "localhost:8000/" e sera redirecionado para o login
## Rodando os testes

Para rodar os testes, rode os seguintes comandos

Entre no container web
```bash
  docker exec -it teste-backend-web-1 bash
```

```bash
  python manage.py test
```

## Documentação da API

#### Toda a documentação swagger

```http
  GET localhost:8000/api
```

#### Autenticacao via JWT

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `Bearer` | `token` | Obtido no acess na rota "/api/token/" |

## Funcionalidades

- Possibilita registro e login
- Estando autenticado possibilita conexao com o google agenda
- Criacao de eventos e agendas no google agenda do usuario
- Criacao de agenda com horarios disponiveis que podem ser consultados e a partir das informacoes criado um novo evento no google agenda