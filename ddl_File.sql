-- جدول‌های پایه


-- جدول شهرها
CREATE TABLE Cities (
    CId SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- جدول ورزش‌ها
CREATE TABLE Sports (
    SId SERIAL PRIMARY KEY,
    SName VARCHAR(50) NOT NULL
);

-- جدول لیگ
CREATE TABLE League (
    LId SERIAL PRIMARY KEY,
    LName VARCHAR(150) NOT NULL,
    SportID INT REFERENCES Sports(SId)
);

-- جدول ورزشگاه
CREATE TABLE Venue (
    VenueID SERIAL PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    CityID INT REFERENCES Cities(CId),
    Capacity INT
);

-- نوع جایگاه
CREATE TABLE SectionType (
    STypeID SERIAL PRIMARY KEY,
    TypeName VARCHAR(100) NOT NULL
);

-- جدول تیم‌ها
CREATE TABLE Teams (
    TeamID SERIAL PRIMARY KEY,
    TName VARCHAR(100) NOT NULL,
    SportID INT REFERENCES Sports(SId)
);

-- جدول کاربران
CREATE TABLE Users (
    UID SERIAL PRIMARY KEY,
    FName VARCHAR(50) NOT NULL,
    LName VARCHAR(50) NOT NULL,
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(30) NOT NULL,
    IsActive BOOLEAN DEFAULT TRUE,
    RegDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- جدول‌های مربوط به مسابقه و بلیط

-- بخش‌های ورزشگاه
CREATE TABLE VenueSection (
    SecID SERIAL PRIMARY KEY,
    VenueID INT REFERENCES Venue(VenueID),
    STypeID INT REFERENCES SectionType(STypeID),
    SecName VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL
);

-- صندلی‌ها
CREATE TABLE Seat (
    SeatID SERIAL PRIMARY KEY,
    SecID INT REFERENCES VenueSection(SecID),
    RowNumber VARCHAR(10),
    SeatNumber INT,
    IsActive INT2
);

-- مسابقات
CREATE TABLE Event (
    EID SERIAL PRIMARY KEY,
    SportID INT REFERENCES Sports(SId),
    LeagueID INT REFERENCES League(LId),
    VenueID INT REFERENCES Venue(VenueID),
    HomeTeam INT REFERENCES Teams(TeamID),
    AwayTeam INT REFERENCES Teams(TeamID),
    EventDate TIMESTAMP NOT NULL,
    Status VARCHAR(30),
    HomeScore INT DEFAULT 0,
    AwayScore INT DEFAULT 0,
    Notes VARCHAR(500)
);

-- کنسلی و تغییر
CREATE TABLE Policy (
    PID SERIAL PRIMARY KEY,
    EID INT REFERENCES Event(EID),
    CancelUntil TIMESTAMP,
    RefundPercent INT,
    Notes VARCHAR(200)
);

-- دسته‌بندی بلیط و قیمت
CREATE TABLE TicketCategory (
    CatID SERIAL PRIMARY KEY,
    EID INT REFERENCES Event(EID),
    SecID INT REFERENCES VenueSection(SecID),
    CatName VARCHAR(50),
    Price INT NOT NULL,
    StartDate TIMESTAMP,
    EndDate TIMESTAMP
);

-- موجودی صندلی‌ها
CREATE TABLE SeatInventory (
    InvID SERIAL PRIMARY KEY,
    EID INT REFERENCES Event(EID),
    SeatID INT REFERENCES Seat(SeatID),
    CatID INT REFERENCES TicketCategory(CatID),
    Status VARCHAR(50),
    ReserveKey VARCHAR(100)
);



-- خرید و لاگ‌ها

-- سفارش خرید
CREATE TABLE "Order" (
    OrderID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UID),
    EID INT REFERENCES Event(EID),
    Status VARCHAR(50),
    OrderDate TIMESTAMP,
    TotalAmount INT
);

-- جزئیات سفارش
CREATE TABLE OrderItem (
    ItemID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES "Order"(OrderID),
    CatID INT REFERENCES TicketCategory(CatID),
    Qty INT,
    Price INT
);

-- بلیط‌های صادرشده
CREATE TABLE Ticket (
    TID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES "Order"(OrderID),
    EID INT REFERENCES Event(EID),
    UID INT REFERENCES Users(UID),
    InvID INT REFERENCES SeatInventory(InvID),
    SerialNum INT NOT NULL,
    Status VARCHAR(50),
    IssueDate TIMESTAMP
);

-- ورود به ورزشگاه
CREATE TABLE CheckInLog (
    LogID SERIAL PRIMARY KEY,
    TID INT REFERENCES Ticket(TID),
    EnterTime TIMESTAMP,
    Gate VARCHAR(50)
);

-- پشتیبانی و گزارش‌ها
CREATE TABLE Report (
    ReportID SERIAL PRIMARY KEY,
    UID INT REFERENCES Users(UID),
    TID INT REFERENCES Ticket(TID),
    Subject VARCHAR(100),
    Message TEXT,
    Status VARCHAR(50)
);

-- پیام‌های ارسالی
CREATE TABLE NotificationOutbox (
    NID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UID),
    Subject VARCHAR(200),
    MsgContent TEXT,
    SendDate TIMESTAMP,
    Status VARCHAR(50)
);