
USE QL_NhaHang
GO 
-- 1. Account
CREATE TABLE Account (
    UserName NVARCHAR(50) PRIMARY KEY,
    DisplayName NVARCHAR(100) NOT NULL,
    Password NVARCHAR(100) NOT NULL,
    Role INT NOT NULL CHECK (Role IN (0,1))
);

-- 2. TableFood
CREATE TABLE TableFood (
    TableID INT IDENTITY(1,1) PRIMARY KEY,
    TableName NVARCHAR(50) NOT NULL,
    Status INT NOT NULL DEFAULT 0
);

-- 3. Category
CREATE TABLE Category (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL
);

-- 4. Food
CREATE TABLE Food (
    FoodID INT IDENTITY(1,1) PRIMARY KEY,
    FoodName NVARCHAR(100) NOT NULL,
    CategoryID INT NOT NULL,
    Price FLOAT NOT NULL CHECK (Price > 0),

    CONSTRAINT FK_Food_Category 
    FOREIGN KEY (CategoryID) 
    REFERENCES Category(CategoryID)
);

-- 5. Bill
CREATE TABLE Bill (
    BillID INT IDENTITY(1,1) PRIMARY KEY,
    DateCheckIn DATETIME NOT NULL DEFAULT GETDATE(),
    DateCheckOut DATETIME NULL,
    TableID INT NOT NULL,
    Status INT NOT NULL DEFAULT 0,
    UserName NVARCHAR(50) NOT NULL,

    CONSTRAINT FK_Bill_Table 
    FOREIGN KEY (TableID) 
    REFERENCES TableFood(TableID),

    CONSTRAINT FK_Bill_Account
    FOREIGN KEY (UserName)
    REFERENCES Account(UserName)
);

-- 6. BillInfo
CREATE TABLE BillInfo (
    BillInfoID INT IDENTITY(1,1) PRIMARY KEY,
    BillID INT NOT NULL,
    FoodID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),

    CONSTRAINT FK_BillInfo_Bill
    FOREIGN KEY (BillID)
    REFERENCES Bill(BillID),

    CONSTRAINT FK_BillInfo_Food
    FOREIGN KEY (FoodID)
    REFERENCES Food(FoodID)
);