fastapi-backend/
│
├── .venv/
│
├── app/
│   ├── config/
│   │   ├── database.py
│   │   ├── redis.py
│   │   └── settings.py
│   │
│   ├── dependencies/
│   │   ├── auth_dependency.py
│   │   └── db_dependency.py
│   │
│   ├── lib/
│   │   ├── jwt.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── refresh_token_model.py
│   │   ├── memory_model.py
│   │   ├── soulmate_model.py
│   │   └── users_model.py
│   │
│   ├── repositories/
│   │   ├── refresh_token_repository.py
│   │   ├── soulmate_repository.py
│   │   ├── memory_repository.py
│   │   ├── memory_retrieval_repository.py
│   │   └── user_repository.py
│   │
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── soulmate_router.py
│   │   ├── chat_router.py
│   │   └── user_router.py
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── chat_schema.py
│   │   ├── memory_schema.py
│   │   ├── soulmate_schema.py
│   │   └── users_schema.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── soulmate_service.py
│   │   ├── llm_service.py
│   │   ├── chat_service.py
│   │   ├── embedding_service.py
│   │   ├── memory_extraction_service.py
│   │   ├── memory_retrieval_service.py
│   │   ├── memory_service.py
│   │   └── user_service.py
│   │
│   ├── services/
│   │   └── memory_worker.py
│   │
│   └── main.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── .env
├── alembic.ini
├── README.md
└── requirements.txt

alembic init migrations  #Create migration folder 
alembic revision --autogenerate -m "create memory table"
alembic upgrade head



