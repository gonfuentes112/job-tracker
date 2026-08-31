Job Tracker API

A REST API for managing job applications, built with Python, FastAPI, PostgreSQL, SQLAlchemy, and Pydantic.

## 🚀 Live Demo

**[→ Try the Live Demo Through Swagger API](https://job-tracker-gbgi.onrender.com/docs)**

Languages:
English | 日本語

<a name="english"></a>

English
Overview

Job Tracker API is a REST API for managing personal job applications.

The API provides user authentication, authorization, CRUD operations for job applications, database migrations, automated testing, and a Docker-based development environment.

The project was built as a portfolio project to practice modern backend development with Python and demonstrate the design and implementation of a production-oriented REST API.

Features
User registration
Password hashing with pwdlib
JWT-based authentication
Protected API endpoints
Per-user authorization
CRUD operations for job applications
Request and response validation with Pydantic
PostgreSQL database
SQLAlchemy ORM
Database migrations with Alembic
Automated tests with pytest
Docker and Docker Compose
GitHub Actions CI
Production deployment with Render
PostgreSQL hosting with Neon
Interactive API documentation with Swagger UI
Tech Stack
Technology	Purpose
Python	Programming language
FastAPI	REST API framework
Pydantic	Data validation and API schemas
SQLAlchemy	ORM and database access
PostgreSQL	Relational database
Alembic	Database migrations
pwdlib	Password hashing
PyJWT	JWT creation and validation
pytest	Automated testing
uv	Python dependency and project management
Docker	Containerization
Docker Compose	Local multi-container environment
GitHub Actions	Continuous integration
Render	API deployment
Neon	PostgreSQL hosting
Architecture

The application follows a layered structure:

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

Authentication follows this flow:

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
Authorization / Ownership Check
Project Structure
job-tracker-api/
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
Authentication and Authorization

The API uses JWT bearer tokens for authentication.

Registration

A user provides an email address and password.

The password is hashed before being stored in the database.

Plain password
      │
      ▼
Password hashing
      │
      ▼
Hashed password
      │
      ▼
PostgreSQL

The original password is never stored.

Login

After providing valid credentials, the API returns an access token:

{
  "access_token": "...",
  "token_type": "bearer"
}

The token is then supplied in the Authorization header:

Authorization: Bearer <token>
Authorization

Authentication determines who the user is.

Authorization determines what that user is allowed to access.

Job applications are associated with their owner through user_id.

Therefore, when retrieving applications, the API only returns applications belonging to the authenticated user.

Database

PostgreSQL is used as the relational database.

SQLAlchemy provides the ORM layer:

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

Alembic is used to manage database schema changes.

For example:

uv run alembic upgrade head

applies all available migrations.

Local Development
Requirements
Python 3.13+
uv
Docker
Docker Compose
Git
Install dependencies

Clone the repository and install the project dependencies:

uv sync

If development dependencies are defined in a development dependency group:

uv sync --dev
Environment variables

Create a .env file in the project root.

Example:

DATABASE_URL=postgresql+psycopg://your_user:your_pass@localhost:5432/job_tracker
SECRET_KEY=your-development-secret
TEST_DATABASE_URL=postgresql+psycopg://your_dev_user:your_dev_pass@localhost:5432/job_tracker_test

Do not commit .env to Git.

Start PostgreSQL

Start the Docker Compose environment:

docker compose up -d
Run migrations

Apply the database migrations:

uv run alembic upgrade head
Start the API
uv run uvicorn app.main:app --reload

The API will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs
Running with Docker Compose

The complete local environment can also be started with:

docker compose up --build

This starts the API and PostgreSQL services.

To stop the environment:

docker compose down

To stop the environment and remove its database volume:

docker compose down -v

Warning: -v removes the PostgreSQL data volume.

Testing

Run the test suite with:

uv run pytest

The tests cover functionality including:

Health checks
User registration
User login
Authentication
Protected endpoints
CRUD operations
User authorization
Application ownership

The project also runs the test suite automatically through GitHub Actions when changes are pushed or pull requests are created.

CI

GitHub Actions is used for continuous integration.

The CI workflow:

Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ├── Install Python
        ├── Install uv
        ├── Start PostgreSQL
        ├── Install dependencies
        └── Run pytest
                │
                ▼
             PASS / FAIL

This helps ensure that changes do not introduce regressions.

Deployment

The API is deployed using Render and the PostgreSQL database is hosted using Neon.

Production configuration is provided through environment variables rather than being stored in the repository.

The production database schema is managed with Alembic migrations.

API Documentation

FastAPI automatically generates interactive OpenAPI documentation.

Once the application is running, visit:

/docs

The Swagger UI can be used to test endpoints, including authenticated endpoints.

Future Improvements

Possible future improvements include:

OAuth2 / OpenID Connect authentication
Refresh tokens
Pagination
Filtering and sorting
Rate limiting
More comprehensive test coverage
Improved error handling
Additional job application fields
Search functionality
License

This project is intended primarily as a portfolio and learning project.

<a name="日本語"></a>

日本語
概要

Job Tracker API は、求人への応募状況を管理するための REST API です。

## 🚀 ライブデモ
**[→ Swagger UIでAPIを試す](https://job-tracker-gbgi.onrender.com/docs)**

ユーザー認証・認可、求人応募情報の CRUD 操作、データベースマイグレーション、自動テスト、Docker を利用した開発環境などを実装しています。

Python によるバックエンド開発、および実用的な REST API の設計・実装を学習するためのポートフォリオプロジェクトとして開発しました。

主な機能
ユーザー登録
pwdlib によるパスワードハッシュ化
JWT による認証
認証が必要な API エンドポイント
ユーザーごとの認可
求人応募情報の CRUD 操作
Pydantic によるリクエスト・レスポンスのバリデーション
PostgreSQL データベース
SQLAlchemy ORM
Alembic によるデータベースマイグレーション
pytest による自動テスト
Docker / Docker Compose
GitHub Actions による CI
Render への API デプロイ
Neon による PostgreSQL ホスティング
Swagger UI による API ドキュメント
技術スタック
技術	用途
Python	プログラミング言語
FastAPI	REST API フレームワーク
Pydantic	データバリデーション・API スキーマ
SQLAlchemy	ORM・データベースアクセス
PostgreSQL	リレーショナルデータベース
Alembic	データベースマイグレーション
pwdlib	パスワードハッシュ化
PyJWT	JWT の生成・検証
pytest	自動テスト
uv	Python の依存関係・プロジェクト管理
Docker	コンテナ化
Docker Compose	ローカルのマルチコンテナ環境
GitHub Actions	継続的インテグレーション
Render	API のデプロイ
Neon	PostgreSQL ホスティング
アーキテクチャ

アプリケーションはレイヤー構造で設計しています。

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

認証処理は以下のように動作します。

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
認可・所有権チェック
プロジェクト構成
job-tracker-api/
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
認証・認可

認証には JWT Bearer Token を使用しています。

ユーザー登録

ユーザーはメールアドレスとパスワードを使用して登録します。

パスワードはデータベースに保存する前にハッシュ化します。

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

元のパスワードそのものはデータベースに保存しません。

ログイン

正しい認証情報を入力すると、API はアクセストークンを返します。

{
  "access_token": "...",
  "token_type": "bearer"
}

その後、認証が必要なリクエストでは以下のようにトークンを送信します。

Authorization: Bearer <token>
認可

認証（Authentication） は、

「このユーザーは誰か？」

を確認する仕組みです。

認可（Authorization） は、

「このユーザーが何を利用できるか？」

を確認する仕組みです。

求人応募情報には user_id が保存され、それぞれの応募情報の所有者を識別します。

そのため、応募情報を取得するときには、認証されたユーザー自身の応募情報だけが返されます。

データベース

リレーショナルデータベースとして PostgreSQL を使用しています。

SQLAlchemy を ORM として利用しています。

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

データベーススキーマの変更には Alembic を使用します。

例えば以下のコマンドでマイグレーションを適用できます。

uv run alembic upgrade head
ローカル開発
必要な環境
Python 3.12+
uv
Docker
Docker Compose
Git
依存関係のインストール

リポジトリを clone した後、以下を実行します。

uv sync

開発用依存関係を別の dependency group に定義している場合：

uv sync --dev
環境変数

プロジェクトのルートディレクトリに .env ファイルを作成します。

例：

DATABASE_URL=postgresql+psycopg://your_user:your_pass@localhost:5432/job_tracker
SECRET_KEY=your-development-secret
TEST_DATABASE_URL=postgresql+psycopg://your_dev_user:your_dev_pass@localhost:5432/job_tracker_test

.env は Git に commit しないでください。

PostgreSQL の起動

Docker Compose を使用して PostgreSQL を起動します。

docker compose up -d
マイグレーション

データベースにマイグレーションを適用します。

uv run alembic upgrade head
API の起動
uv run uvicorn app.main:app --reload

API は以下で利用できます。

http://localhost:8000

インタラクティブな API ドキュメント：

http://localhost:8000/docs
Docker Compose

API と PostgreSQL を Docker Compose で起動できます。

docker compose up --build

停止する場合：

docker compose down

コンテナと PostgreSQL のデータボリュームを削除する場合：

docker compose down -v

注意: -v を使用すると PostgreSQL のデータボリュームが削除されます。

テスト

pytest を使用してテストを実行します。

uv run pytest

以下のような機能をテストしています。

Health check
ユーザー登録
ユーザーログイン
認証
認証が必要なエンドポイント
CRUD 操作
ユーザーごとの認可
応募情報の所有権

また、GitHub Actions によって push や pull request の際に自動的にテストが実行されます。

CI

継続的インテグレーション（CI）には GitHub Actions を使用しています。

ワークフローは以下のように動作します。

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

これにより、コード変更によって既存の機能が壊れていないかを自動的に確認できます。

デプロイ

API は Render にデプロイし、PostgreSQL データベースは Neon でホスティングしています。

本番環境の設定値はリポジトリに保存せず、環境変数として設定しています。

本番データベースのスキーマ変更は Alembic によって管理しています。

API ドキュメント

FastAPI は OpenAPI に基づいた API ドキュメントを自動生成します。

アプリケーション起動後、以下にアクセスできます。

/docs

Swagger UI を使用して、認証が必要な API を含め、各エンドポイントをブラウザからテストできます。

今後の改善

今後の改善候補：

OAuth2 / OpenID Connect
Refresh Token
Pagination
Filtering / Sorting
Rate Limiting
テストカバレッジの向上
エラーハンドリングの改善
求人応募情報の項目追加
検索機能
ライセンス

このプロジェクトは主にポートフォリオおよび学習目的で作成しています。

⬆ Back to top / ページ上部へ