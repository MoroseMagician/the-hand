DROP DATABASE IF EXISTS the_hand;
CREATE DATABASE the_hand
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE the_hand;

CREATE TABLE haha_nice_meme_my_friend(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(256),
    url VARCHAR(1024), -- urls can be stupidly long
    message TEXT,
    filename VARCHAR(64),
    timestamp DATETIME
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
