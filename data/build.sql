CREATE TABLE IF NOT EXISTS player (
    user_id integer PRIMARY KEY,
    join_date text,
    balance integer DEFAULT 10000,
    win_count integer DEFAULT 0,
    loss_count integer DEFAULT 0,
    exp integer DEFAULT 0,
    lvl integer DEFAULT 1
);