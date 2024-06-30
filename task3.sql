-- The database used is sqlite3

--command to create Category table
CREATE TABLE Category (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Category VARCHAR(50) NOT NULL
);

--command to add values in the Category table
INSERT INTO Category (Category) VALUES ('Energy');

--command to create Index_Master table
CREATE TABLE Index_Master (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(150) NOT NULL,
    Frequency VARCHAR(2) NOT NULL CHECK (Frequency IN ('D', 'M', 'W')),
    Category_ID INTEGER NOT NULL,
    FOREIGN KEY (Category_ID) REFERENCES Category(ID)
);

--command to add values in the Index_Master table
INSERT INTO Index_Master (Name, Frequency, Category_ID)
VALUES ('Solar Power', 'D', 1),
       ('Thermal Power', 'M', 1),
       ('Wind Power', 'M', 1),
       ('Solar Power', 'M', 1),
       ('Solar Power', 'M', 1);

--command to create Sector_Date
CREATE TABLE Sector_Data (
    Index_Master_ID INT NOT NULL,
    Date DATE NOT NULL,
    Value DECIMAL(25,5) NOT NULL,
    FOREIGN KEY (Index_Master_ID) REFERENCES Index_Master(ID)
);

--get all the field in Category
select * from Category

--get all the field in Index_Master
select * from Index_Master

--get all the fields in the Sector_Date
Select * from Sector_Data

-- command to add values to Sector_Data
INSERT INTO Sector_Data (Index_Master_ID, Date, Value)
VALUES 
(1, '2024-06-30', 2435.55),
(2, '2023-03-31', 253.12),
(3, '2024-05-31', 9697.23),
(4, '2024-05-31', 123.14),
(5, '2024-06-30', 323.14);

--task 3(b)
select * from Category, Index_Master, Sector_Data
where Category.ID == Index_Master.Category_ID and Index_Master.ID == Sector_Data.Index_Master_ID And
Category.Category = 'China_Energy' and Index_Master.Frequency = 'D' and Sector_Data.Date LIKE '2024%'

--task 3(c.1) (Average)
select Index_Master.Name, avg(Sector_Data.Value) from Category, Index_Master, Sector_Data
where Category.ID == Index_Master.Category_ID and Index_Master.ID == Sector_Data.Index_Master_ID And
Index_Master.Frequency = 'M' AND Index_Master.Name = 'Solar Power'
GROUP by Index_Master.Name

--task 3(c.2) Median
WITH SortedValues AS (
    SELECT Value,
           ROW_NUMBER() OVER (ORDER BY Value) AS RowNum,
           COUNT(*) OVER () AS TotalRows
    FROM Sector_Data
    JOIN Index_Master ON Sector_Data.Index_Master_ID = Index_Master.ID
    WHERE Index_Master.Frequency = 'M'
      AND Index_Master.Name = 'Solar Power'
)
SELECT AVG(Value) AS Median
FROM SortedValues
WHERE RowNum IN ((TotalRows + 1) / 2, (TotalRows + 2) / 2);
