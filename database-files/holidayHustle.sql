
DROP DATABASE IF EXISTS HolidayHustle;

CREATE DATABASE IF NOT EXISTS HolidayHustle;

USE HolidayHustle;
CREATE TABLE users
(
    UserID integer PRIMARY KEY AUTO_INCREMENT,
    Name varChar(50),
    LastSeen datetime,
    MarkedForRemoval boolean
);

INSERT INTO users VALUES(1, 'Barbara Murphy', '2025-03-14 18:06:19', FALSE);
INSERT INTO users VALUES(2, 'Jason Smith', '2025-04-01 13:26:21', FALSE);
INSERT INTO users VALUE(3, 'Carlos Ramirez', '2023-03-04 20:20:20', TRUE);



CREATE TABLE apps (
    AppID integer PRIMARY KEY
);

INSERT INTO apps VALUES (1);
INSERT INTO apps VALUES (2);

CREATE TABLE accounts
(
    AccountID integer PRIMARY KEY,
    AccountType varchar(50) NOT NULL,
    ProfilePicture varchar(50),
    ProfileDescription varchar(128),
    UserID integer,
    FOREIGN KEY (userID) REFERENCES users (userID),
    AppID integer,
    FOREIGN KEY (AppID) REFERENCES apps (AppID)
);

INSERT INTO accounts VALUES(1,
'Normal','Good old Barbara Murphy smiling' ,'Im Barbara
    and I love planning events for my family, friends and children', 1, 1);
INSERT INTO accounts VALUES(2,
'Normal','Event planning company logo Jason works at' ,'I have
worked at Events Co. for more than 7 years', 2, 1);
INSERT INTO accounts VALUES(3,
'Data Analyst','A professional smiling photo of Carlos Ramirez'
                               ,'NO DESCRIPTION', 3, 1);


CREATE TABLE subscription
(
    Pro varchar(50),
    Free varchar(50),
    AccountID integer NOT NULL,
    FOREIGN KEY (AccountID) REFERENCES accounts (AccountID)
);

INSERT INTO subscription VALUES ('Has Pro Version', 'Not using Free Version', 1);
INSERT INTO subscription VALUES ('Has Pro Version', 'Not using Free Version', 1);
INSERT INTO subscription VALUES ('Does not have Pro Version', 'Currently using Free Version', 1);




CREATE TABLE personalInformation
(
    PersonalID integer PRIMARY KEY AUTO_INCREMENT,
    Name varchar(255),
    DOB date,
    UserID integer,
    FOREIGN KEY (UserID) REFERENCES users (UserID)
);

INSERT INTO personalInformation VALUES (1, 'Barbara Murphy', '1968-02-14', 1);
INSERT INTO personalInformation VALUES (2, 'Jason Smith', '1987-08-22', 2);
INSERT INTO personalInformation VALUES (3, 'Carlos Ramirez', '1996-06-26', 3);


CREATE TABLE personalizedSuggestions (
    SuggestionID integer PRIMARY KEY AUTO_INCREMENT,
    Allergies varchar(255),
    GroupSize integer,
    AppID integer,
    Popularity integer,
    Audience varchar(255),
    FOREIGN KEY (AppID) REFERENCES apps(AppID)
);

INSERT INTO personalizedSuggestions
VALUES (1, 'Peanuts, Soy', 8, 1, 89, 'Family and Friends');
INSERT INTO personalizedSuggestions
VALUES(2,
       'Tree Nuts', 12, 1, 68, 'Coworkers');
INSERT INTO personalizedSuggestions
VALUES (3, 'None', 3, 1, 93, 'Immediate Family');

CREATE TABLE presets
(
    PresetID integer PRIMARY KEY AUTO_INCREMENT,
    Date datetime,
    Name varchar(255),
    UserID integer,
    SuggestionID integer,
    FOREIGN KEY (UserID) REFERENCES users (UserID),
    FOREIGN KEY (SuggestionID) REFERENCES personalizedSuggestions (SuggestionID)
);

INSERT INTO presets VALUES (1, '2025-04-01 14:30:00', 'April Fools at Work p1', 1, 2);
INSERT INTO presets VALUES (2, '2021-12-25 14:30:00', 'Christmas p1', 3, 1);

CREATE TABLE presetSuggestions
(
    SuggestionID int,
    PresetID int,
    FOREIGN KEY (SuggestionID) REFERENCES personalizedSuggestions (SuggestionID),
    FOREIGN KEY (PresetID) REFERENCES presets (PresetID)
);


CREATE TABLE complaints
(
    ComplaintID integer PRIMARY KEY,
    ComplaintText varchar(500),
    UserID integer,
    AppID integer,
    FOREIGN KEY (UserID) REFERENCES users (UserID),
    FOREIGN KEY (AppID) REFERENCES apps (AppID)
);

INSERT INTO complaints
VALUES (1, 'There are too many adds on this site', 1, 1);
INSERT INTO complaints
VALUES(2,
       'I wish there were more personalized suggestions I could choose from', 2, 1);
INSERT INTO complaints
VALUES (3, 'I wish the interface was clearer', 3, 1);

CREATE TABLE inputs
(
    AppID integer,
    Popularity integer,
    InputID integer PRIMARY KEY AUTO_INCREMENT,
    FOREIGN KEY (AppID) REFERENCES apps (AppID)
);

INSERT INTO inputs
VALUES(1, 98, 1);
INSERT INTO inputs
VALUES (1, 78, 2);
INSERT INTO inputs
VALUES (1, 87, 3);

CREATE TABLE holidays
(
    HolidayID integer PRIMARY KEY,
    popularity integer,
    Name VARCHAR(255),
    SuggestionID integer,
    Date date,
    FOREIGN KEY (SuggestionID) REFERENCES personalizedSuggestions (SuggestionID)
);

INSERT INTO holidays VALUES(1, 100, 'Halloween', 1, '2025-10-31');
INSERT INTO holidays VALUES(2, 82, 'Earth Day', 2, '2025-4-22');
INSERT INTO holidays VALUES(3, 100, 'Christmas', 3, '2025-12-25');

CREATE TABLE foodDecoActivities
(
    Popularity integer,
    Pricing integer,
    Dates datetime,
    Clicks integer,
    FDAID integer PRIMARY KEY
);

CREATE TABLE SuggestionsFDA
(
    SuggestionID int,
    FDAID int,
    FOREIGN KEY (SuggestionID) REFERENCES personalizedSuggestions (SuggestionID),
    FOREIGN KEY (FDAID) REFERENCES foodDecoActivities (FDAID)
);

CREATE TABLE HolidayFDA
(
    HolidayID int,
    FDAID int,
    FOREIGN KEY (HolidayID) REFERENCES holidays (HolidayID),
    FOREIGN KEY (FDAID) REFERENCES foodDecoActivities (FDAID)
);

INSERT INTO foodDecoActivities
VALUES(96, 750, '2025-12-24', 37453, 1);
INSERT INTO foodDecoActivities
VALUES(91, 250, '2025-11-1', 21386, 2);

CREATE TABLE exportLogs (
    LogID integer PRIMARY KEY AUTO_INCREMENT,
    Files varchar(255),
    AccountID Integer,
    DateExported datetime,
    FOREIGN KEY (AccountID) REFERENCES accounts(AccountID)
);
INSERT INTO exportLogs VALUES(1, 'Daily Revenue in 2021', 3, '2022-03-01 17:23:10');
INSERT INTO exportLogs VALUES(2, 'Active Users per Country in 2022', 3, '2023-01-20 9:17:50');

CREATE TABLE visuals (
    VisualID integer PRIMARY KEY AUTO_INCREMENT,
    Color varchar(50),
    Shape varchar(50),
    IsWritable boolean,
    Length decimal(5,2),
    Width decimal(5,2),
    SuggestionID integer,
    FOREIGN KEY (SuggestionID) REFERENCES personalizedSuggestions(SuggestionID)
);

INSERT INTO visuals
    values(1, 'Blue', 'Rectangle', true, 50, 25,  1);
INSERT INTO visuals
    values(2, 'Red', 'Circle', false, 10, 10,  1);

CREATE TABLE inputHistory (
    inputID int,
    inputMade date,
    MarkedForRemoval boolean,
    FOREIGN KEY (inputID) REFERENCES inputs(inputID)
);


-- SQL STATEMENTS --
    -- PERSONA 1
#1.1
SELECT ps.SuggestionID, ps.GroupSize, FDA.pricing
FROM personalizedSuggestions ps
JOIN SuggestionsFDA sf ON ps.SuggestionID = sf.SuggestionID
JOIN foodDecoActivities FDA ON sf.FDAID = FDA.FDAID
WHERE ps.GroupSize >= 20
   AND FDA.Pricing <= 500;
#1.2
INSERT INTO complaints
VALUES (00231, 'I was given a non-gluten free recipe although I specified a gluten free allergy',
       1, 1);

#1.3
SELECT ps.SuggestionID
FROM personalizedSuggestions ps
WHERE ps.Allergies = 'Gluten';

#1.4
SELECT ps.SuggestionID, FDA.Popularity, FDA.Clicks
FROM personalizedSuggestions ps
JOIN SuggestionsFDA sf ON ps.SuggestionID = sf.SuggestionID
JOIN foodDecoActivities FDA ON sf.FDAID = FDA.FDAID
WHERE FDA.Popularity >= 4 AND FDA.Clicks >= 20;

#1.5
UPDATE presets p
JOIN personalizedSuggestions ps ON p.SuggestionID = ps.SuggestionID
SET ps.GroupSize = 25
WHERE p.PresetID = 1225 AND p.UserID = 1;

#1.6
UPDATE subscription s
JOIN accounts a ON s.AccountID = a.AccountID
SET s.Pro = 'TRUE', s.Free = 'FALSE'
WHERE a.AccountID = 1 AND a.UserID = 1;



    -- PERSONA 2
-- 1. As a planner, I would like to be able to see all the suggestions the app gives when placing certain parameters
    SELECT DISTINCT ps.SuggestionID
    FROM  inputs i JOIN apps a on i.AppID = a.AppID
    JOIN personalizedSuggestions ps on a.AppID = ps.AppID;

-- 2. As a planner, I would like to see what previous parameters I inputted into the app
    SELECT DISTINCT ih.InputID
    FROM inputs i JOIN inputHistory ih on i.InputID = ih.inputID;

-- 3. As a planner, I would like to be able to remove selected previous parameters
DELETE inputHistory
FROM inputHistory
    WHERE inputHistory.MarkedForRemoval = true;

-- 4. As a planner, I would like to see the price of the suggested decorations, food,
-- and activities relative to a given price range
    SELECT fda.Pricing
    FROM personalizedSuggestions ps JOIN foodDecoActivities fda on ps.SuggestionID = fda.SuggestionID
    WHERE 25 < fda.Pricing < 50; -- Example of a price range

-- 5. As a planner, I would like to see the most popular items for the given parameters,
    SELECT *
    FROM personalizedSuggestions ps JOIN foodDecoActivities f on ps.SuggestionID = f.SuggestionID
    ORDER BY f.Popularity
    LIMIT 5; -- Cut Off example

-- 6. As a planner, I would like to see what are popular parameters
SELECT ps.Popularity
FROM  personalizedSuggestions ps
ORDER BY  ps.Popularity
LIMIT 5; -- Cut Off example

    -- PERSONA 3
    -- 3.1: Average pricing and total clicks per holiday
SELECT
   h.Name AS HolidayName,
   AVG(f.Pricing) AS AvgSpending,
   SUM(f.Clicks) AS TotalClicks
FROM
   foodDecoActivities f
JOIN
   holidays h ON f.HolidayID = h.HolidayID
GROUP BY
   h.Name;


-- 3.2: Top 10 suggestions by popularity and clicks with visual data
SELECT
   s.SuggestionID,
   s.Popularity,
   f.Clicks,
   f.Dates,
   v.Color,
   v.Shape
FROM
   personalizedSuggestions s
LEFT JOIN
   visuals v ON s.SuggestionID = v.SuggestionID
LEFT JOIN
   foodDecoActivities f ON s.SuggestionID = f.SuggestionID
ORDER BY
   s.Popularity DESC, f.Clicks DESC
LIMIT 10;


-- 3.3: Average pricing per group size (proxy for budget)
SELECT
   s.GroupSize,
   AVG(f.Pricing) AS AvgBudgetAllocation
FROM
   personalizedSuggestions s
JOIN
   foodDecoActivities f ON s.SuggestionID = f.SuggestionID
GROUP BY
   s.GroupSize;


-- 3.4: Suggestions created per calendar month
SELECT
   MONTH(p.Date) AS Month,
   COUNT(p.SuggestionID) AS TotalSuggestions
FROM
   presets p
GROUP BY
   MONTH(p.Date)
ORDER BY
   Month;


-- 3.5: Export user selections with app and suggestion details
SELECT
   u.UserID,
   a.AppID,
   s.SuggestionID,
   s.Allergies,
   s.GroupSize,
   s.Popularity
FROM
   users u
JOIN
   accounts ac ON u.UserID = ac.UserID
JOIN
   apps a ON a.AppID = ac.AppID
JOIN
   personalizedSuggestions s ON s.AppID = a.AppID;


-- 3.6: Spending by group type
SELECT
   CASE
       WHEN s.GroupSize <= 5 THEN 'Casual Host'
       ELSE 'Professional Planner'
   END AS HostType,
   AVG(f.Pricing) AS AvgSpending
FROM
   personalizedSuggestions s
JOIN
   foodDecoActivities f ON s.SuggestionID = f.SuggestionID
GROUP BY
   HostType;

    -- PERSONA 4
-- Removing inactive users
UPDATE users u JOIN accounts a on u.UserID = a.UserID
SET u.MarkedForRemoval = TRUE
WHERE u.LastSeen < DATE_SUB(NOW(), INTERVAL 3 YEAR);
SELECT * FROM users WHERE users.MarkedForRemoval = TRUE;

UPDATE users u JOIN accounts a on u.UserID = a.UserID
SET u.MarkedForRemoval = FALSE
WHERE u.UserID = 1;

-- DELETE FROM users  WHERE users.MarkedForRemoval = true;

-- Updating the interface
    -- PERSONALIZED SUGGESTIONS DOESNT HAVE ANY DATA SO THIS CANT RUN

INSERT INTO visuals (VisualID, Color, Shape, IsWritable, Length, Width, SuggestionID)
VALUES (4, 'Blue', 'Rectangle', TRUE, 10.5, 5.5,  2);
SELECT * FROM visuals;

UPDATE visuals
SET Color = 'GREEN', SHAPE = 'CIRCLE'
WHERE VisualID = 4;
DELETE FROM visuals WHERE VisualID = 4;

-- Adding new searches
INSERT INTO presets(DATE, NAME, USERID, SUGGESTIONID)
VALUES (NOW(), 'Family-Friendly Events', 3,2);
SELECT * FROM presets;

UPDATE presets
SET Name = 'Kid-Friendly Events'
WHERE PresetID = 2;

DELETE FROM presets WHERE PresetID = 2;

-- Adding monetization methods
INSERT INTO  subscription (Pro, Free, AccountID)
VALUES ('Ad Free Premium', 'Basic with Ads', 3);
SELECT * FROM subscription;

UPDATE subscription
SET Pro = 'PREMIUM+ (Exclusive Content)', Free = 'Basic with Limited Access'
WHERE AccountID = 3;

-- Displaying most popular events
INSERT INTO foodDecoActivities (Popularity, Pricing, Dates, Clicks, SuggestionID, HolidayID)
VALUES (100, 50, NOW(), 5000, 2, 3);

SELECT * FROM foodDecoActivities ORDER BY Popularity DESC LIMIT 5;

UPDATE foodDecoActivities
SET Popularity = Popularity + 10
WHERE HolidayID = 10;

-- TRACKING common complaints from users
INSERT INTO complaints (ComplaintID, ComplaintText, UserID, AppID)
VALUES (4,'App crashes frequently on Android', 2,1);
SELECT complaints.ComplaintText, COUNT(*) AS Frequency
FROM complaints
GROUP BY ComplaintText
ORDER BY Frequency DESC;

UPDATE complaints
SET ComplaintText = CONCAT(ComplaintText, '-[RESOLVED')
WHERE ComplaintID = 4;
DELETE FROM complaints WHERE ComplaintID = 4