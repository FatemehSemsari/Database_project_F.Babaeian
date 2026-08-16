CREATE TABLE Cities (
    CId SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

CREATE TABLE Sports (
    SId SERIAL PRIMARY KEY,
    SName VARCHAR(50) NOT NULL
);

CREATE TABLE League (
    LId SERIAL PRIMARY KEY,
    LName VARCHAR(150) NOT NULL,
    SportID INT REFERENCES Sports(SId)
);


CREATE TABLE Venue (
    VenueID SERIAL PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    CityID INT REFERENCES Cities(CId),
    Capacity INT
);


CREATE TABLE SectionType (
    STypeID SERIAL PRIMARY KEY,
    TypeName VARCHAR(100) NOT NULL
);


CREATE TABLE Teams (
    TeamID SERIAL PRIMARY KEY,
    TName VARCHAR(100) NOT NULL,
    SportID INT REFERENCES Sports(SId)
);


DROP TABLE IF EXISTS users;


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



CREATE TABLE VenueSection (
    SecID SERIAL PRIMARY KEY,
    VenueID INT REFERENCES Venue(VenueID),
    STypeID INT REFERENCES SectionType(STypeID),
    SecName VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL
);


CREATE TABLE Seat (
    SeatID SERIAL PRIMARY KEY,
    SecID INT REFERENCES VenueSection(SecID),
    RowNumber VARCHAR(10),
    SeatNumber INT,
    IsActive INT2
);


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


CREATE TABLE Policy (
    PID SERIAL PRIMARY KEY,
    EID INT REFERENCES Event(EID),
    CancelUntil TIMESTAMP,
    RefundPercent INT,
    Notes VARCHAR(200)
);


CREATE TABLE TicketCategory (
    CatID SERIAL PRIMARY KEY,
    EID INT REFERENCES Event(EID),
    SecID INT REFERENCES VenueSection(SecID),
    CatName VARCHAR(50),
    Price INT NOT NULL,
    StartDate TIMESTAMP,
    EndDate TIMESTAMP
);


CREATE TABLE SeatInventory (
    InvID SERIAL PRIMARY KEY,
    EID INT REFERENCES Event(EID),
    SeatID INT REFERENCES Seat(SeatID),
    CatID INT REFERENCES TicketCategory(CatID),
    Status VARCHAR(50),
    ReserveKey VARCHAR(100)
);



CREATE TABLE "Order" (
    OrderID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UID),
    EID INT REFERENCES Event(EID),
    Status VARCHAR(50),
    OrderDate TIMESTAMP,
    TotalAmount INT
);


CREATE TABLE OrderItem (
    ItemID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES "Order"(OrderID),
    CatID INT REFERENCES TicketCategory(CatID),
    Qty INT,
    Price INT
);


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


CREATE TABLE CheckInLog (
    LogID SERIAL PRIMARY KEY,
    TID INT REFERENCES Ticket(TID),
    EnterTime TIMESTAMP,
    Gate VARCHAR(50)
);


CREATE TABLE Report (
    ReportID SERIAL PRIMARY KEY,
    UID INT REFERENCES Users(UID),
    TID INT REFERENCES Ticket(TID),
    Subject VARCHAR(100),
    Message TEXT,
    Status VARCHAR(50)
);


CREATE TABLE NotificationOutbox (
    NID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UID),
    Subject VARCHAR(200),
    MsgContent TEXT,
    SendDate TIMESTAMP,
    Status VARCHAR(50)
);

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,

    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20) UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    role VARCHAR(30) NOT NULL DEFAULT 'customer',

    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    phone_verified BOOLEAN NOT NULL DEFAULT FALSE,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    city_id INT NULL REFERENCES cities(cid),
    birth_date DATE NULL,
    profile_image_url VARCHAR(500) NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_users_identifier
        CHECK (email IS NOT NULL OR phone IS NOT NULL),

    CONSTRAINT chk_users_role
        CHECK (role IN ('customer', 'support')),

    CONSTRAINT chk_email_verified
        CHECK (
            email_verified = FALSE
            OR email IS NOT NULL
        ),

    CONSTRAINT chk_phone_verified
        CHECK (
            phone_verified = FALSE
            OR phone IS NOT NULL
        )
);


ALTER TABLE "Order"
RENAME COLUMN userid TO user_id;

ALTER TABLE "Order"
ADD CONSTRAINT fk_order_user
FOREIGN KEY (user_id)
REFERENCES users(id);


ALTER TABLE ticket
RENAME COLUMN uid TO user_id;

ALTER TABLE ticket
ADD CONSTRAINT fk_ticket_user
FOREIGN KEY (user_id)
REFERENCES users(id);


ALTER TABLE report
RENAME COLUMN uid TO user_id;

ALTER TABLE report
ADD CONSTRAINT fk_report_user
FOREIGN KEY (user_id)
REFERENCES users(id);


ALTER TABLE notificationoutbox
RENAME COLUMN userid TO user_id;

ALTER TABLE notificationoutbox
ADD CONSTRAINT fk_notification_user
FOREIGN KEY (user_id)
REFERENCES users(id);


ALTER TABLE cities
ADD COLUMN province VARCHAR(100);

ALTER TABLE teams
ADD COLUMN city_id INT REFERENCES cities(cid);


ALTER TABLE seat
ALTER COLUMN isactive TYPE BOOLEAN
USING (isactive <> 0);

ALTER TABLE seat
ALTER COLUMN isactive SET DEFAULT TRUE;


ALTER TABLE seat
ADD CONSTRAINT uq_seat_section_row_number
UNIQUE (secid, rownumber, seatnumber);


ALTER TABLE event
ADD CONSTRAINT chk_event_different_teams
CHECK (hometeam <> awayteam);

ALTER TABLE policy
ADD CONSTRAINT chk_refund_percent
CHECK (
    refundpercent >= 0
    AND refundpercent <= 100
);

ALTER TABLE ticketcategory
ADD CONSTRAINT chk_ticket_category_price
CHECK (price >= 0);

ALTER TABLE ticketcategory
ADD CONSTRAINT chk_ticket_category_dates
CHECK (
    enddate IS NULL
    OR startdate IS NULL
    OR enddate > startdate
);

ALTER TABLE seatinventory
ADD COLUMN held_until TIMESTAMP NULL;

ALTER TABLE seatinventory
ADD CONSTRAINT uq_event_seat_inventory
UNIQUE (eid, seatid);

ALTER TABLE "Order"
ADD COLUMN expires_at TIMESTAMP NULL;

ALTER TABLE "Order"
ADD COLUMN paid_at TIMESTAMP NULL;


CREATE TABLE payment (
    id SERIAL PRIMARY KEY,

    order_id INT NOT NULL
        REFERENCES "Order"(orderid),

    amount INT NOT NULL,

    method VARCHAR(30) NOT NULL,

    status VARCHAR(30) NOT NULL,

    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    paid_at TIMESTAMP NULL,

    transaction_ref VARCHAR(100),

    CONSTRAINT chk_payment_amount
        CHECK (amount >= 0),

    CONSTRAINT chk_payment_status
        CHECK (
            status IN (
                'pending',
                'successful',
                'failed',
                'refunded'
            )
        )
);


ALTER TABLE ticket
ADD CONSTRAINT uq_ticket_serial
UNIQUE (serialnum);

ALTER TABLE ticket
ADD CONSTRAINT uq_ticket_inventory
UNIQUE (invid);


CREATE TABLE amenity (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE section_amenity (
    section_id INT
        REFERENCES venuesection(secid),

    amenity_id INT
        REFERENCES amenity(id),

    PRIMARY KEY (
        section_id,
        amenity_id
    )
);


BEGIN;

CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    iso_code VARCHAR(10) UNIQUE
);

CREATE TABLE provinces (
    province_id SERIAL PRIMARY KEY,
    country_id INT NOT NULL
        REFERENCES countries(country_id),
    name VARCHAR(100) NOT NULL,

    CONSTRAINT uq_province_country_name
        UNIQUE (country_id, name)
);

ALTER TABLE cities
ADD COLUMN province_id INT;

ALTER TABLE cities
ADD CONSTRAINT fk_city_province
FOREIGN KEY (province_id)
REFERENCES provinces(province_id);

ALTER TABLE cities
DROP COLUMN province;

COMMIT;


ALTER TABLE league
ADD COLUMN season VARCHAR(20);

ALTER TABLE league
ADD COLUMN start_date DATE;

ALTER TABLE league
ADD COLUMN end_date DATE;

ALTER TABLE league
ADD CONSTRAINT chk_league_dates
CHECK (
    start_date IS NULL
    OR end_date IS NULL
    OR end_date >= start_date
);


CREATE TABLE league_team (
    league_id INT NOT NULL
        REFERENCES league(lid)
        ON DELETE CASCADE,

    team_id INT NOT NULL
        REFERENCES teams(teamid)
        ON DELETE CASCADE,

    PRIMARY KEY (
        league_id,
        team_id
    )
);


ALTER TABLE teams
ADD COLUMN logo_url VARCHAR(500);


ALTER TABLE venue
ADD COLUMN address VARCHAR(500);

CREATE UNIQUE INDEX uq_league_sport_name_season
ON league (
    sportid,
    lname,
    season
)
WHERE season IS NOT NULL;



BEGIN;

-- 1) Order -> Reservation

ALTER TABLE "Order"
RENAME TO reservation;

ALTER TABLE reservation
RENAME COLUMN orderid TO reservation_id;

ALTER TABLE reservation
RENAME COLUMN eid TO event_id;

ALTER TABLE reservation
RENAME COLUMN orderdate TO reserved_at;

ALTER TABLE reservation
RENAME COLUMN totalamount TO total_amount;


-- 2) OrderItem -> ReservationItem

ALTER TABLE orderitem
RENAME TO reservation_item;

ALTER TABLE reservation_item
RENAME COLUMN itemid TO item_id;

ALTER TABLE reservation_item
RENAME COLUMN orderid TO reservation_id;

ALTER TABLE reservation_item
RENAME COLUMN catid TO cat_id;


-- 3) Ticket -> Reservation

ALTER TABLE ticket
RENAME COLUMN orderid TO reservation_id;


-- 4) Payment -> Reservation
-- 

ALTER TABLE payment
RENAME COLUMN order_id TO reservation_id;


-- 5) Reservation time validation

ALTER TABLE reservation
ALTER COLUMN reserved_at
SET DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE reservation
ADD CONSTRAINT chk_reservation_expiry
CHECK (
    expires_at IS NULL
    OR reserved_at IS NULL
    OR expires_at >= reserved_at
);


-- 6) ReservationItem validation

ALTER TABLE reservation_item
ADD CONSTRAINT chk_reservation_item_qty
CHECK (qty > 0);

ALTER TABLE reservation_item
ADD CONSTRAINT chk_reservation_item_price
CHECK (price >= 0);


-- 7) Reservation total amount validation

ALTER TABLE reservation
ADD CONSTRAINT chk_reservation_total_amount
CHECK (
    total_amount IS NULL
    OR total_amount >= 0
);


-- 8) Connect held SeatInventory to Reservation

ALTER TABLE seatinventory
ADD COLUMN reservation_id INT NULL;

ALTER TABLE seatinventory
ADD CONSTRAINT fk_seatinventory_reservation
FOREIGN KEY (reservation_id)
REFERENCES reservation(reservation_id)
ON DELETE SET NULL;


-- 9) Remove duplicated User/Event from Ticket


ALTER TABLE ticket
DROP COLUMN user_id;

ALTER TABLE ticket
DROP COLUMN eid;


-- 10) Report can also refer to a Reservation

ALTER TABLE report
ADD COLUMN reservation_id INT NULL;

ALTER TABLE report
ADD CONSTRAINT fk_report_reservation
FOREIGN KEY (reservation_id)
REFERENCES reservation(reservation_id)
ON DELETE SET NULL;

COMMIT;


CREATE TABLE reservation_seat (
    reservation_id INT NOT NULL
        REFERENCES reservation(reservation_id)
        ON DELETE CASCADE,

    inventory_id INT NOT NULL
        REFERENCES seatinventory(invid),

    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (
        reservation_id,
        inventory_id
    )
);


CREATE SEQUENCE IF NOT EXISTS ticket_serial_number_seq
START WITH 100000;


CREATE TABLE organizer (
    organizer_id SERIAL PRIMARY KEY,

    name VARCHAR(150) NOT NULL UNIQUE,

    description TEXT NULL,

    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE event
ADD COLUMN organizer_id INT NOT NULL
REFERENCES organizer(organizer_id);



CREATE TABLE cancellation_rule (
    rule_id SERIAL PRIMARY KEY,

    organizer_id INT NOT NULL
        REFERENCES organizer(organizer_id),

    min_hours_before_event NUMERIC(10, 2)
        NOT NULL,

    max_hours_before_event NUMERIC(10, 2)
        NULL,

    refund_percent SMALLINT
        NOT NULL,

    can_cancel BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    is_active BOOLEAN
        NOT NULL
        DEFAULT TRUE,

    notes TEXT NULL,

    created_at TIMESTAMP
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_cancellation_min_hours
        CHECK (
            min_hours_before_event >= 0
        ),

    CONSTRAINT chk_cancellation_max_hours
        CHECK (
            max_hours_before_event IS NULL
            OR max_hours_before_event >
               min_hours_before_event
        ),

    CONSTRAINT chk_cancellation_refund_percent
        CHECK (
            refund_percent >= 0
            AND refund_percent <= 100
        ),

    CONSTRAINT chk_non_cancelable_refund
        CHECK (
            can_cancel = TRUE
            OR refund_percent = 0
        )
);


CREATE TABLE wallet (
    wallet_id SERIAL PRIMARY KEY,

    user_id INT NOT NULL UNIQUE
        REFERENCES users(id),

    balance BIGINT NOT NULL DEFAULT 0,

    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_wallet_balance
        CHECK (balance >= 0)
);



ALTER TABLE payment
ADD COLUMN refund_amount BIGINT NULL;

ALTER TABLE payment
ADD COLUMN refunded_at TIMESTAMP NULL;

ALTER TABLE payment
ADD CONSTRAINT chk_payment_refund_amount
CHECK (
    refund_amount IS NULL
    OR refund_amount >= 0
);



ALTER TABLE report
ADD COLUMN support_response TEXT NULL;

ALTER TABLE report
ADD COLUMN reviewed_by INT NULL
    REFERENCES users(id);

ALTER TABLE report
ADD COLUMN reviewed_at TIMESTAMP NULL;


ALTER TABLE reservation
ADD COLUMN support_review_status VARCHAR(30)
NOT NULL DEFAULT 'unreviewed';

ALTER TABLE reservation
ADD COLUMN support_reviewed_by INT NULL
    REFERENCES users(id);

ALTER TABLE reservation
ADD COLUMN support_reviewed_at TIMESTAMP NULL;

ALTER TABLE reservation
ADD COLUMN support_note TEXT NULL;

ALTER TABLE reservation
ADD CONSTRAINT chk_reservation_support_review_status
CHECK (
    support_review_status IN (
        'unreviewed',
        'approved',
        'modified',
        'cancelled'
    )
);










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