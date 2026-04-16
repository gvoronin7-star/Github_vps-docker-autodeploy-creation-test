# Настройка GitHub Actions для деплоя

## Секреты репозитория

Перед использованием workflow необходимо настроить секреты в репозитории GitHub:

### 1. Зайди в настройки репозитория
- Перейди: `Settings` → `Secrets and variables` → `Actions`
- Нажми `New repository secret` для каждого секрета

### 2. Необходимые секреты

| Имя секрета | Описание | Пример |
|-------------|----------|--------|
| `SSH_HOST` | IP-адрес или домен сервера | `192.168.1.100` или `myserver.com` |
| `SSH_USER` | Имя пользователя SSH | `ubuntu` или `root` |
| `SSH_KEY` | Приватный SSH-ключ для доступа | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `SSH_PORT` | Порт SSH (опционально) | `22` (по умолчанию) |

### 3. Как получить SSH-ключ

**На сервере:**
```bash
# Создать пару ключей (если нет)
ssh-keygen -t ed25519 -C "github-actions@deploy"

# Показать публичный ключ
cat ~/.ssh/id_ed25519.pub

# Показать приватный ключ (для секрета SSH_KEY)
cat ~/.ssh/id_ed25519
```

**Добавить публичный ключ на сервер:**
```bash
# На локальной машине
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Вставить в GitHub:**
- Скопируй полный приватный ключ (включая `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`)
- Вставь в секрете `SSH_KEY`

## Структура workflow

```
┌─────────────────────────┐
│  build-and-push         │
│  (Сборка образа)        │
│  ─────────────────────  │
│  1. Checkout            │
│  2. Login to GHCR       │
│  3. Build Docker image  │
│  4. Push to registry    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  deploy                 │
│  (Развёртывание)        │
│  ─────────────────────  │
│  1. Checkout            │
│  2. Login to GHCR       │
│  3. SSH to server       │
│  4. Pull new image      │
│  5. Stop old container  │
│  6. Start new container │
│  7. Verify deployment   │
└─────────────────────────┘
```

## Путь к образу в GHCR

Образ будет доступен по адресу:
```
ghcr.io/{username}/{repository}:{tag}
```

Пример:
```
ghcr.io/gvoronin7-star/system__1:main-abc123
ghcr.io/gvoronin7-star/system__1:latest
```

## Триггеры

- `push` на ветку `main` → запуск обеих джоб
- `pull_request` на ветку `main` → только сборка (без деплоя)

## Управление контейнером

Имя контейнера на сервере: `fastapi-time-server`

### Полезные команды на сервере:

```bash
# Проверка статуса
docker ps | grep fastapi-time-server

# Просмотр логов
docker logs -f fastapi-time-server

# Перезапуск
docker restart fastapi-time-server

# Остановка
docker stop fastapi-time-server

# Удаление
docker rm fastapi-time-server
```

## Troubleshooting

### Ошибка подключения по SSH
- Проверь, что SSH-ключ добавлен в `authorized_keys` на сервере
- Убедись, что порт SSH открыт в фаерволе
- Проверь `SSH_HOST` и `SSH_USER`
- **Локальный доступ:** Убедись, что SSH-ключ лежит в корне проекта и имеет правильные права

### Ошибка доступа к registry
- `GITHUB_TOKEN` создаётся автоматически
- Убедись, что в workflow указаны правильные `permissions`

### Контейнер не запускается
- Проверь логи: `docker logs fastapi-time-server`
- Убедись, что порт 8000 свободен на сервере
- Проверь переменные окружения
