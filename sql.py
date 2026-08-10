#نمایش فهرست ورزشگاه‌ها به همراه شهر
SportTicket_VenueCatalogQuery = """
SELECT
    venue_id,
    name AS venue_name,
    city
FROM "Venue"
ORDER BY city, name;
"""

#نمایش فهرست شهرهای دارای ورزشگاه
SportTicket_CityCatalogQuery = """
SELECT DISTINCT city
FROM "Venue"
WHERE city IS NOT NULL
ORDER BY city;
"""

#نمایش فهرست تیم‌ها به همراه شهر
SportTicket_TeamCatalogQuery = """
SELECT
    team_id,
    name AS team_name,
    city
FROM "Team"
ORDER BY name;
"""

#نمایش فهرست رشته‌های ورزشی
SportTicket_SportCatalogQuery = """
SELECT
    sport_id,
    name AS sport_name
FROM "Sport"
ORDER BY name;
"""

#نمایش لیگ‌ها به همراه رشتهٔ ورزشی مربوطه
SportTicket_LeagueCatalogQuery = """
SELECT
    l.league_id,
    l.name AS league_name,
    s.name AS sport_name
FROM "League" AS l, "Sport" AS s
WHERE s.sport_id = l.sport_id
ORDER BY s.name, l.name;
"""

#نمایش فهرست مسابقات آینده
SportTicket_UpcomingMatchListQuery = """
SELECT
    e.event_id,
    s.name AS sport_name,
    l.name AS league_name,
    home.name AS home_team,
    away.name AS away_team,
    v.name AS venue_name,
    v.city,
    e.event_date,
    e.start_time
FROM "Event" AS e, "Sport" AS s, "League" AS l, "Venue" AS v, "Team" AS home, "Team" AS away
WHERE e.sport_id = s.sport_id
  AND e.league_id = l.league_id
  AND e.venue_id = v.venue_id
  AND e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND e.event_date >= CURRENT_DATE
ORDER BY e.event_date, e.start_time;
"""

#جست‌وجوی مسابقات برگزارشونده در یک شهر مشخص
SportTicket_CityMatchFinderQuery = """
SELECT
    e.event_id,
    home.name AS home_team_name,
    away.name AS away_team_name,
    v.name AS venue_name,
    v.city,
    e.event_date,
    e.start_time
FROM "Event" AS e, "Venue" AS v, "Team" AS home, "Team" AS away
WHERE e.venue_id = v.venue_id
  AND e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND v.city = %s
  AND e.status = 'scheduled'
ORDER BY e.event_date, e.start_time;
"""

#جست‌وجوی مسابقات یک تیم مشخص
SportTicket_TeamMatchFinderQuery = """
SELECT
    e.event_id,
    home.name AS home_team,
    away.name AS away_team,
    e.event_date,
    e.start_time,
    v.name AS venue_name,
    v.city
FROM "Event" AS e, "Team" AS home, "Team" AS away, "Venue" AS v
WHERE e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND e.venue_id = v.venue_id
  AND (home.name LIKE '%' || :team_name || '%'
       OR away.name LIKE '%' || :team_name || '%')
ORDER BY e.event_date, e.start_time;
"""

#جست‌وجوی مسابقات مربوط به یک رشتهٔ ورزشی مشخص
SportTicket_SportMatchFinderQuery = """
SELECT
    e.event_id,
    s.name AS sport_name,
    home.name AS home_team,
    away.name AS away_team,
    l.name AS league_name,
    v.name AS venue_name,
    v.city,
    e.event_date,
    e.start_time
FROM "Event" AS e, "Sport" AS s, "Team" AS home, "Team" AS away, "League" AS l, "Venue" AS v
WHERE e.sport_id = s.sport_id
  AND e.home_team_id = home.team_id
  AND e.away_team_id = away.team_id
  AND e.league_id = l.league_id
  AND e.venue_id = v.venue_id
  AND s.name = :sport_name
ORDER BY e.event_date, e.start_time;
"""

#نمایش کاربرانی که هیچ رزروی ثبت نکرده‌اند
SportTicket_UsersWithoutReservationQuery = """
SELECT u.first_name, u.last_name
FROM Users u
WHERE NOT EXISTS (
    SELECT 1
    FROM Reservation r
    WHERE r.user_id = u.user_id
);
"""

#نمایش کاربرانی که حداقل یک رزرو فعال دارند
SportTicket_UsersWithActiveReservationQuery = """
SELECT u.first_name, u.last_name
FROM Users u
WHERE EXISTS (
    SELECT 1
    FROM Reservation r
    WHERE r.user_id = u.user_id
      AND r.status = 'active'
);
"""

#محاسبهٔ مجموع پرداخت هر کاربر به تفکیک ماه
SportTicket_UserMonthlyPaymentQuery = """
SELECT r.user_id, p.payment_month, SUM(p.amount) AS total_paid
FROM Reservation r, Payment p
WHERE r.reservation_id = p.reservation_id
GROUP BY r.user_id, p.payment_month
ORDER BY r.user_id, p.payment_month;
"""

#نمایش کاربرانی که در هر شهر دقیقاً یک خرید موفق داشته‌اند
SportTicket_OnePurchasePerCityQuery = """
SELECT r.user_id, v.city
FROM Reservation r, Event e, Venue v
WHERE r.event_id = e.event_id
  AND e.venue_id = v.venue_id
  AND r.status = 'active'
GROUP BY r.user_id, v.city
HAVING COUNT(r.reservation_id) = 1;
"""

#نمایش اطلاعات خریدار آخرین بلیط ثبت‌شده
SportTicket_LatestTicketBuyerQuery = """
SELECT u.first_name, u.last_name, r.created_at
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND r.created_at = (
      SELECT MAX(created_at)
      FROM Reservation
  );
"""

#نمایش کاربرانی که مجموع پرداختشان بیشتر از میانگین کل پرداخت‌ها است
SportTicket_HighSpendingUsersQuery = """
SELECT r.user_id, SUM(p.amount) AS total_spent
FROM Reservation r, Payment p
WHERE r.reservation_id = p.reservation_id
GROUP BY r.user_id
HAVING SUM(p.amount) > (
    SELECT AVG(amount)
    FROM Payment
);
"""