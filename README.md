# Job Tracker API

A REST API for managing personal job applications, built with Python, FastAPI, PostgreSQL, SQLAlchemy, and Pydantic.

## 🚀 Live Demo

[→ Try the Live Demo Through Swagger UI](https://job-tracker-gbgi.onrender.com/docs)

Languages:

**English** | [日本語](#日本語)

<a name="english"></a>

# English

## Overview

Job Tracker API is a REST API for managing personal job applications.

The API provides user authentication, per-user authorization, CRUD operations for job applications, database migrations, automated testing, CI, and a Docker-based development environment.

The project was built as a portfolio project to practice modern backend development with Python and demonstrate the design and implementation of a production-oriented REST API.

## Features

* User registration
* Secure password hashing with `pwdlib`
* JWT-based authentication
* JWT expiration and validation
* Protected API endpoints
* Per-user resource authorization
* Ownership checks to prevent unauthorized cross-user access
* CRUD operations for job applications
* Request and response validation with Pydantic
* SQL injection-safe database access through SQLAlchemy
* PostgreSQL database
* SQLAlchemy ORM
* Database migrations with Alembic
* Automated tests with pytest
* Ruff linting and formatting
* Pyrefly type checking
* Docker and Docker Compose
* GitHub Actions CI
* Production deployment with Render
* PostgreSQL hosting with Neon
* Interactive API documentation with Swagger UI

## Tech Stack

| Technology     | Purpose                                  |
| -------------- | ---------------------------------------- |
| Python         | Programming language                     |
| FastAPI        | REST API framework                       |
| Pydantic       | Data validation and API schemas          |
| SQLAlchemy     | ORM and database access                  |
| PostgreSQL     | Relational database                      |
| Alembic        | Database migrations                      |
| pwdlib         | Password hashing                         |
| PyJWT          | JWT creation and validation              |
| pytest         | Automated testing                        |
| Ruff           | Linting and code formatting              |
| Pyrefly        | Static type checking                     |
| uv             | Python dependency and project management |
| Docker         | Containerization                         |
| Docker Compose | Local multi-container environment        |
| GitHub Actions | Continuous integration                   |
| Render         | API deployment                           |
| Neon           | PostgreSQL hosting                       |

## Architecture

The application follows a layered structure:

```text
Client
  │
  ▼
FastAPI Routers
  │
  ▼
Service Layer
  │
  ▼
SQLAlchemy Models
  │
  ▼
PostgreSQL
```

Authentication and authorization follow this flow:

```text
Login Request
     │
     ▼
Verify Password
     │
     ▼
Create JWT
     │
     ▼
Client receives access token
     │
     ▼
Protected Request
     │
     ▼
get_current_user()
     │
     ▼
Identify User
     │
     ▼
Ownership / Authorization Check
     │
     ▼
Access only authorized resources
```

## Authentication and Authorization

The API uses JWT bearer tokens for authentication.

### Registration

A user provides an email address and password.

The password is hashed before being stored in the database:

```text
Plain Password
      │
      ▼
Password Hashing
      │
      ▼
Hashed Password
      │
      ▼
PostgreSQL
```

The original password is never stored.

### Login

After providing valid credentials, the API returns an access token:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

The token is then supplied in the `Authorization` header:

```text
Authorization: Bearer <token>
```

JWTs include an expiration time and are validated when protected endpoints are accessed.

Invalid, expired, malformed, or otherwise unusable tokens are rejected.

### Authorization and Resource Ownership

Authentication determines **who the user is**.

Authorization determines **what the user is allowed to access**.

Each job application is associated with its owner through `user_id`.

For operations on a specific application, the API checks both the requested application ID and the authenticated user's ID:

```text
application_id
      +
current_user.id
      │
      ▼
Authorized resource
```

This prevents users from accessing, modifying, or deleting another user's applications by manipulating an application ID.

The test suite specifically verifies cross-user access protection.

## Input Validation and Error Handling

Pydantic schemas validate incoming request data, including required fields and length constraints.

The API also avoids exposing unnecessary internal information through authentication and resource errors.

For example, login failures use a generic authentication error rather than revealing whether a specific email address exists.

## Database

PostgreSQL is used as the relational database.

SQLAlchemy provides the ORM and database access layer:

```text
FastAPI
   │
   ▼
Service Layer
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
```

Alembic is used to manage database schema changes.

For example:

```bash
uv run alembic upgrade head
```

applies all available migrations.

## Project Structure

```text
job-tracker/
├── app/
│   ├── api/          # API routers and endpoints
│   ├── core/         # Configuration, security, dependencies
│   ├── db/           # Database configuration and session management
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic request/response schemas
│   └── services/     # Business logic
├── tests/            # Automated tests and fixtures
├── alembic/          # Database migration files
├── .github/
│   └── workflows/    # GitHub Actions workflows
├── Dockerfile
├── compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```

## Local Development

### Requirements

* Python 3.13+
* uv
* Docker
* Docker Compose
* Git

### Install Dependencies

Clone the repository and install the project dependencies:

```bash
uv sync
```

Development dependencies are included through the `dev` dependency group.

### Environment Variables

Create a `.env` file in the project root.

Example:

```text
DATABASE_URL=postgresql+psycopg://your_user:your_pass@localhost:5432/job_tracker
SECRET_KEY=your-development-secret
TEST_DATABASE_URL=postgresql+psycopg://your_dev_user:your_dev_pass@localhost:5432/job_tracker_test
```

Do not commit `.env` to Git.

For production, configuration values are provided through environment variables.

### Start PostgreSQL

Start the Docker Compose environment:

```bash
docker compose up -d
```

### Run Migrations

```bash
uv run alembic upgrade head
```

### Start the API

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Running with Docker Compose

The complete local environment can also be started with:

```bash
docker compose up --build
```

This starts the API and PostgreSQL services.

To stop the environment:

```bash
docker compose down
```

To stop the environment and remove the PostgreSQL data volume:

```bash
docker compose down -v
```

> **Warning:** `-v` removes the PostgreSQL data volume.

## Testing

Run the test suite with:

```bash
uv run pytest
```

The tests cover:

* Health checks
* User registration
* Password hashing
* User login
* Authentication failures
* JWT validation and expiration
* Protected endpoints
* CRUD operations
* Request validation
* Per-user authorization
* Application ownership
* Cross-user access prevention
* Unauthorized update and delete attempts
* SQL injection-related authentication input

The project also runs the test suite automatically through GitHub Actions when changes are pushed or pull requests are created.

## Code Quality

The project uses automated static analysis and formatting tools:

```bash
ruff check .
ruff format --check .
uv run pyrefly check
```

These checks help identify code-quality issues, formatting problems, and type errors before changes are committed.

## CI

GitHub Actions is used for continuous integration.

The CI workflow follows this general process:

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ├── Install Python
        ├── Install uv
        ├── Start PostgreSQL
        ├── Install dependencies
        └── Run tests
                │
                ▼
             PASS / FAIL
```

This helps ensure that changes do not introduce regressions.

## Deployment

The API is deployed using Render and the PostgreSQL database is hosted using Neon.

Production configuration is provided through environment variables rather than being stored in the repository.

The production database schema is managed with Alembic migrations.

## API Documentation

FastAPI automatically generates interactive OpenAPI documentation.

Once the application is running, visit:

```text
/docs
```

Swagger UI can be used to inspect and test the API, including authenticated endpoints.

## Future Improvements

Possible future improvements include:

* Integration with an external identity provider using OAuth 2.0 / OpenID Connect
* Refresh tokens
* Pagination
* Filtering and sorting
* Rate limiting
* Expanded test coverage
* Additional job application fields
* Search functionality

## License

This project is intended primarily as a portfolio and learning project.

---

<a name="日本語"></a>

# 日本語

[↑ English](#english)

## 概要

Job Tracker API は、個人の求人応募情報を管理するための REST API です。

ユーザー認証・ユーザーごとの認可、求人応募情報の CRUD 操作、データベースマイグレーション、自動テスト、CI、Docker を利用した開発環境などを実装しています。

Python によるバックエンド開発を学習し、実用的な REST API の設計・実装を実践するためのポートフォリオプロジェクトとして開発しました。

## 主な機能

* ユーザー登録
* `pwdlib` による安全なパスワードハッシュ化
* JWT による認証
* JWT の有効期限・トークン検証
* 認証が必要な API エンドポイント
* ユーザーごとのリソース認可
* 所有権チェックによる他ユーザーのリソースへの不正アクセス防止
* 求人応募情報の CRUD 操作
* Pydantic によるリクエスト・レスポンスのバリデーション
* SQLAlchemy による SQL インジェクション対策を考慮したデータベースアクセス
* PostgreSQL
* SQLAlchemy ORM
* Alembic によるデータベースマイグレーション
* pytest による自動テスト
* Ruff による lint・フォーマット
* Pyrefly による型チェック
* Docker / Docker Compose
* GitHub Actions による CI
* Render への API デプロイ
* Neon による PostgreSQL ホスティング
* Swagger UI による API ドキュメント

## 技術スタック

| 技術             | 用途                    |
| -------------- | --------------------- |
| Python         | プログラミング言語             |
| FastAPI        | REST API フレームワーク      |
| Pydantic       | データバリデーション・API スキーマ   |
| SQLAlchemy     | ORM・データベースアクセス        |
| PostgreSQL     | リレーショナルデータベース         |
| Alembic        | データベースマイグレーション        |
| pwdlib         | パスワードハッシュ化            |
| PyJWT          | JWT の生成・検証            |
| pytest         | 自動テスト                 |
| Ruff           | lint・コードフォーマット        |
| Pyrefly        | 静的型チェック               |
| uv             | Python の依存関係・プロジェクト管理 |
| Docker         | コンテナ化                 |
| Docker Compose | ローカルのマルチコンテナ環境        |
| GitHub Actions | 継続的インテグレーション          |
| Render         | API のデプロイ             |
| Neon           | PostgreSQL ホスティング     |

## アーキテクチャ

アプリケーションは以下のレイヤー構造で設計しています。

```text
Client
  │
  ▼
FastAPI Routers
  │
  ▼
Service Layer
  │
  ▼
SQLAlchemy Models
  │
  ▼
PostgreSQL
```

認証・認可は以下のように処理されます。

```text
ログインリクエスト
      │
      ▼
パスワード検証
      │
      ▼
JWT 生成
      │
      ▼
アクセストークンをクライアントへ返却
      │
      ▼
認証が必要なリクエスト
      │
      ▼
get_current_user()
      │
      ▼
ユーザーを特定
      │
      ▼
所有権・認可チェック
      │
      ▼
許可されたリソースのみアクセス
```

## 認証・認可

認証には JWT Bearer Token を使用しています。

### ユーザー登録

ユーザーはメールアドレスとパスワードを使用して登録します。

パスワードはデータベースに保存する前にハッシュ化します。

```text
平文パスワード
      │
      ▼
パスワードハッシュ化
      │
      ▼
ハッシュ化されたパスワード
      │
      ▼
PostgreSQL
```

元のパスワードそのものはデータベースに保存しません。

### ログイン

正しい認証情報を入力すると、API はアクセストークンを返します。

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

認証が必要なリクエストでは、以下のようにトークンを送信します。

```text
Authorization: Bearer <token>
```

JWT には有効期限が設定されており、認証が必要なエンドポイントでトークンの有効性を検証します。

期限切れ、不正、形式が不正なトークンなどは拒否されます。

### 認可・リソース所有権

認証（Authentication）は、

**「このユーザーは誰か？」**

を確認する仕組みです。

認可（Authorization）は、

**「このユーザーが何にアクセスできるか？」**

を確認する仕組みです。

求人応募情報には `user_id` が保存され、それぞれの応募情報の所有者を識別します。

特定の応募情報を操作する場合、API は応募情報の ID だけでなく、認証されたユーザーの ID も確認します。

```text
application_id
      +
current_user.id
      │
      ▼
アクセス可能なリソース
```

これにより、応募情報の ID を変更するだけで他ユーザーの応募情報を取得・変更・削除するような不正アクセスを防止しています。

テストでも、ユーザー間の不正アクセスができないことを確認しています。

## 入力バリデーション・エラーハンドリング

Pydantic スキーマによって、必須項目や文字列の長さなど、リクエストデータのバリデーションを行っています。

また、認証エラーやリソースが存在しない場合などに、不要な内部情報を外部へ公開しないようにしています。

例えばログイン失敗時には、特定のメールアドレスが登録されているかどうかを推測しにくいよう、一般的な認証エラーを返します。

## データベース

リレーショナルデータベースとして PostgreSQL を使用しています。

SQLAlchemy を ORM およびデータベースアクセス層として利用しています。

```text
FastAPI
   │
   ▼
Service Layer
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
```

データベーススキーマの変更には Alembic を使用します。

例えば以下のコマンドでマイグレーションを適用できます。

```bash
uv run alembic upgrade head
```

## プロジェクト構成

```text
job-tracker/
├── app/
│   ├── api/          # API ルーター・エンドポイント
│   ├── core/         # 設定・セキュリティ・依存関係
│   ├── db/           # データベース設定・セッション管理
│   ├── models/       # SQLAlchemy モデル
│   ├── schemas/      # Pydantic スキーマ
│   └── services/     # ビジネスロジック
├── tests/            # 自動テスト・fixtures
├── alembic/          # データベースマイグレーション
├── .github/
│   └── workflows/    # GitHub Actions の設定
├── Dockerfile
├── compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```

## ローカル開発

### 必要な環境

* Python 3.13+
* uv
* Docker
* Docker Compose
* Git

### 依存関係のインストール

リポジトリを clone した後、以下を実行します。

```bash
uv sync
```

開発用依存関係は `dev` dependency group に定義されています。

### 環境変数

プロジェクトのルートディレクトリに `.env` ファイルを作成します。

例：

```text
DATABASE_URL=postgresql+psycopg://your_user:your_pass@localhost:5432/job_tracker
SECRET_KEY=your-development-secret
TEST_DATABASE_URL=postgresql+psycopg://your_dev_user:your_dev_pass@localhost:5432/job_tracker_test
```

`.env` は Git に commit しないでください。

本番環境では環境変数を使用して設定値を提供します。

### PostgreSQL の起動

Docker Compose を使用して PostgreSQL を起動します。

```bash
docker compose up -d
```

### マイグレーション

```bash
uv run alembic upgrade head
```

### API の起動

```bash
uv run uvicorn app.main:app --reload
```

API は以下で利用できます。

```text
http://localhost:8000
```

インタラクティブな API ドキュメント：

```text
http://localhost:8000/docs
```

## Docker Compose

API と PostgreSQL を Docker Compose で起動できます。

```bash
docker compose up --build
```

停止する場合：

```bash
docker compose down
```

コンテナと PostgreSQL のデータボリュームを削除する場合：

```bash
docker compose down -v
```

> **注意:** `-v` を使用すると PostgreSQL のデータボリュームが削除されます。

## テスト

pytest を使用してテストを実行します。

```bash
uv run pytest
```

以下のような機能をテストしています。

* Health check
* ユーザー登録
* パスワードハッシュ化
* ユーザーログイン
* 認証エラー
* JWT の検証・有効期限
* 認証が必要なエンドポイント
* CRUD 操作
* リクエストバリデーション
* ユーザーごとの認可
* 応募情報の所有権
* ユーザー間の不正アクセス防止
* 他ユーザーの応募情報への変更・削除の拒否
* SQL インジェクションを想定した認証入力

また、GitHub Actions によって push や pull request の際に自動的にテストが実行されます。

## コード品質

静的解析・フォーマットには以下のツールを使用しています。

```bash
ruff check .
ruff format --check .
uv run pyrefly check
```

これらにより、コード品質、フォーマット、型エラーなどを変更前に確認できます。

## CI

継続的インテグレーション（CI）には GitHub Actions を使用しています。

ワークフローは以下のように動作します。

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ├── Python のセットアップ
        ├── uv のインストール
        ├── PostgreSQL の起動
        ├── 依存関係のインストール
        └── pytest の実行
                │
                ▼
             PASS / FAIL
```

これにより、コード変更によって既存の機能が壊れていないかを自動的に確認できます。

## デプロイ

API は Render にデプロイし、PostgreSQL データベースは Neon でホスティングしています。

本番環境の設定値はリポジトリに保存せず、環境変数として設定しています。

本番データベースのスキーマ変更は Alembic によって管理しています。

## API ドキュメント

FastAPI は OpenAPI に基づいた API ドキュメントを自動生成します。

アプリケーション起動後、以下にアクセスできます。

```text
/docs
```

Swagger UI を使用して、認証が必要な API を含め、各エンドポイントをブラウザからテストできます。

## 今後の改善

今後の改善候補：

* 外部 Identity Provider との OAuth 2.0 / OpenID Connect 連携
* Refresh Token
* Pagination
* Filtering / Sorting
* Rate Limiting
* テストカバレッジの向上
* 求人応募情報の項目追加
* 検索機能

## ライセンス

このプロジェクトは主にポートフォリオおよび学習目的で作成しています。

[↑ ページ上部へ](#english)
