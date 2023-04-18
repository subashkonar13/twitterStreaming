DROP TABLE  IF EXISTS Tweet_Data;
DROP TABLE  IF EXISTS Trending_Data;


CREATE TABLE IF NOT EXISTS Tweet_Data (
    Sno Serial,
	user_id BIGINT PRIMARY KEY,
    tweet_id BIGINT,
	tweet_text text,
	sentiment text,
	comp float,
	Emoticon text,
	created_at TIMESTAMPTZ,
	IngestionTime TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS Trending_Data (
    Sno Serial,
    trend_name text PRIMARY KEY,
	url text,
	tweet_volume BIGINT,
	IngestionTime TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
