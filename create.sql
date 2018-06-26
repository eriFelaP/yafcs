CREATE TABLE `cards` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`question`	TEXT NOT NULL UNIQUE,
	`answer`	TEXT NOT NULL,
	`cdate`	TEXT NOT NULL,
	`efactor`	REAL NOT NULL CHECK(efactor >= 1.3 AND efactor <= 2.5),
	`reps`	INTEGER NOT NULL,
	`inter`	INTEGER NOT NULL,
	`revdate`	TEXT NOT NULL,
	`trials`    INTEGER NOT NULL,
	`quality`   REAL NOT NULL CHECK(quality >= 0 AND quality <= 5),
    `note` TEXT NOT NULL
);