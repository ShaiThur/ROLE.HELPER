CREATE TABLE session (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE user_session_history (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    answer_embedding vector(1024),
    creation_date TIMESTAMP NOT NULL,
    is_description BOOLEAN DEFAULT FALSE
);