CREATE TABLE IF NOT EXISTS Tweet_Data (
    --Sno Serial,
    id BIGINT PRIMARY KEY,
	tweet_text text,
	created_at TIMESTAMPTZ
	--,IngestionTime TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Tweet_Data_pys (
    Sno Serial,
    id BIGINT PRIMARY KEY,
	tweet_text text,
	created_at TIMESTAMPTZ,
	IngestionTime TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);