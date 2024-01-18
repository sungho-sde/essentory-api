INSERT INTO accounts_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
VALUES
('john_doe', 'John', 'Doe', 'john.doe@example.com', 'plaintextpassword', 0, 1, 0, '2024-01-17 10:00:00', '2024-01-17 10:00:00'),
('jane_doe', 'Jane', 'Doe', 'jane.doe@example.com', 'plaintextpassword', 0, 1, 0, '2024-01-17 10:00:00', '2024-01-17 10:00:00'),
('bob_smith', 'Bob', 'Smith', 'bob.smith@example.com', 'plaintextpassword', 0, 1, 0, '2024-01-17 10:00:00', '2024-01-17 10:00:00'),
('alice_jones', 'Alice', 'Jones', 'alice.jones@example.com', 'plaintextpassword', 0, 1, 0, '2024-01-17 10:00:00', '2024-01-17 10:00:00'),
('charlie_brown', 'Charlie', 'Brown', 'charlie.brown@example.com', 'plaintextpassword', 0, 1, 0, '2024-01-17 10:00:00', '2024-01-17 10:00:00');

INSERT INTO channels_channel (name, description, created_at)
VALUES
('Channel 1', 'Description for Channel 1', '2024-01-17 10:00:00'),
('Channel 2', 'Description for Channel 2', '2024-01-17 11:00:00'),
('Channel 10', 'Description for Channel 10', '2024-01-18 10:00:00');

INSERT INTO channels_channel_owners (channel_id, user_id)
VALUES
(1, 1),
(2, 1),
(2, 2),
(2, 10),
(10, 10);

INSERT INTO posts_post (user_id, channel_id, content, created_at, updated_at)
VALUES
(1, 1, 'Sample Post Content 1', '2024-01-17 12:00:00', '2024-01-17 12:00:00'),
(2, 2, 'Sample Post Content 2 by user 2 in channel 2', '2024-01-17 13:00:00', '2024-01-17 13:00:00'),
(1, 2, 'Sample Post Content 3 by user 1 in channel 2', '2024-01-17 13:00:00', '2024-01-17 13:00:00'),
(10, 2, 'Sample Post Content 4 by user 10 in channel 2', '2024-01-17 13:00:00', '2024-01-17 13:00:00'),
(10, 10, 'Sample Post Content 5 by user 10 in channel 10', '2024-01-18 12:00:00', '2024-01-18 12:00:00');

INSERT INTO posts_comment (user_id, post_id, parent_comment_id, content, created_at, updated_at)
VALUES
(1, 1, NULL, 'Sample Comment Content 1  by user 1 for post 1', '2024-01-17 14:00:00', '2024-01-17 14:00:00'),
(2, 2, NULL, 'Sample Comment Content 2  by user 2 for post 2', '2024-01-17 15:00:00', '2024-01-17 15:00:00'),
(1, 2, NULL, 'Sample Comment Content 3  by user 1 for post 2', '2024-01-17 15:00:00', '2024-01-17 15:00:00'),
(10, 2, NULL, 'Sample Comment Content 4  by user 10 for post 2', '2024-01-17 15:00:00', '2024-01-17 15:00:00'),
(10, 10, NULL, 'Sample Comment Content 5 by user 10 for post 5', '2024-01-18 14:00:00', '2024-01-18 14:00:00'),
(1, 2, NULL, 'Nested Comment Content 6  by user 1 for post 2', '2024-01-17 15:00:00', '2024-01-17 15:00:00'),
(1, 2, NULL, 'Nested Comment Content 7  by user 1 for post 2', '2024-01-17 15:00:00', '2024-01-17 15:00:00');
