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

#محاسبهٔ تعداد بلیط‌های فروخته‌شده به تفکیک رشتهٔ ورزشی
SportTicket_TicketsSoldPerSportQuery = """
SELECT s.name AS sport_name, COUNT(r.reservation_id) AS tickets_sold
FROM Reservation r, Event e, Sport s
WHERE r.event_id = e.event_id
  AND e.sport_id = s.sport_id
  AND r.status = 'active'
GROUP BY s.sport_id, s.name;
"""

#نمایش کاربران با بیشترین تعداد خرید در یک بازهٔ زمانی مشخص
SportTicket_TopBuyersInPeriodQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS ticket_count
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND r.created_at >= '2026-08-04 00:00:00'
GROUP BY u.user_id, u.first_name, u.last_name
ORDER BY ticket_count DESC;
"""

#محاسبهٔ آمار فروش بلیط در شهرهای استان تهران
SportTicket_TehranProvinceSalesQuery = """
SELECT v.city, COUNT(r.reservation_id) AS tickets_sold
FROM Reservation r, Event e, Venue v
WHERE r.event_id = e.event_id
  AND e.venue_id = v.venue_id
  AND v.province = 'تهران'
  AND r.status = 'active'
GROUP BY v.city;
"""

#نمایش شهرهای مسابقاتی که قدیمی‌ترین کاربر سامانه برای آن‌ها رزرو داشته است
SportTicket_OldestUserVisitedCitiesQuery = """
SELECT DISTINCT v.city
FROM Reservation r, Event e, Venue v
WHERE r.event_id = e.event_id
  AND e.venue_id = v.venue_id
  AND r.user_id = (
      SELECT user_id
      FROM Users
      WHERE created_at = (
          SELECT MIN(created_at)
          FROM Users
      )
  );
"""

#نمایش فهرست اعضای تیم پشتیبانی سامانه
SportTicket_SupportStaffListQuery = """
SELECT first_name, last_name, email
FROM Users
WHERE role = 'support'
ORDER BY last_name, first_name;
"""

#نمایش کاربران وفادار با حداقل دو خرید فعال
SportTicket_LoyalUsersQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS total_tickets
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND r.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(r.reservation_id) >= 2;
"""

#نمایش کاربرانی که حداکثر دو بلیط فوتبال خریده‌اند
SportTicket_UsersWithAtMostTwoFootballTicketsQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS ticket_count
FROM Users u, Reservation r, Event e, Sport s
WHERE u.user_id = r.user_id
  AND r.event_id = e.event_id
  AND e.sport_id = s.sport_id
  AND s.name = 'فوتبال'
  AND r.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(r.reservation_id) <= 2;
"""

#نمایش کاربرانی که از تمام رشته‌های فوتبال، والیبال و بسکتبال بلیط خریده‌اند
SportTicket_AllSportsBuyersQuery = """
SELECT u.first_name, u.last_name
FROM Users u, Reservation r, Event e, Sport s
WHERE u.user_id = r.user_id
  AND r.event_id = e.event_id
  AND e.sport_id = s.sport_id
  AND s.name IN ('فوتبال', 'والیبال', 'بسکتبال')
  AND r.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(DISTINCT s.sport_id) = 3;
"""

#نمایش رزروهای ثبت‌شده در تاریخ مشخص
SportTicket_TodayReservationsQuery = """
SELECT reservation_id, user_id, event_id, created_at
FROM Reservation
WHERE created_at >= '2026-08-11 00:00:00'
  AND created_at <= '2026-08-11 23:59:59'
ORDER BY created_at ASC;
"""

#نمایش مسابقه یا مسابقات با دومین میزان فروش بلیط
SportTicket_SecondBestSellingEventQuery = """
SELECT event_id, COUNT(reservation_id) AS ticket_count
FROM Reservation
WHERE status = 'active'
GROUP BY event_id
HAVING COUNT(reservation_id) = (
    SELECT MAX(sub.sales_count)
    FROM (
        SELECT COUNT(r2.reservation_id) AS sales_count
        FROM Reservation r2
        WHERE r2.status = 'active'
        GROUP BY r2.event_id
    ) sub
    WHERE sub.sales_count < (
        SELECT MAX(all_sales.sales_count)
        FROM (
            SELECT COUNT(r3.reservation_id) AS sales_count
            FROM Reservation r3
            WHERE r3.status = 'active'
            GROUP BY r3.event_id
        ) all_sales
    )
);
"""

#نمایش عضو پشتیبانی با بیشترین تعداد رزرو لغوشده
SportTicket_SupportWithMostCancellationsQuery = """
SELECT u.first_name, u.last_name, COUNT(r.reservation_id) AS cancellation_count
FROM Users u, Reservation r
WHERE u.user_id = r.user_id
  AND u.role = 'support'
  AND r.status = 'cancelled'
GROUP BY u.user_id, u.first_name, u.last_name
HAVING COUNT(r.reservation_id) = (
    SELECT MAX(temp.cxl_count)
    FROM (
        SELECT COUNT(r2.reservation_id) AS cxl_count
        FROM Users u2, Reservation r2
        WHERE u2.user_id = r2.user_id
          AND u2.role = 'support'
          AND r2.status = 'cancelled'
        GROUP BY u2.user_id
    ) temp
);
"""

#تغییر نام خانوادگی کاربر دارای بیشترین لغو رزرو به Reddington
SportTicket_UpdateReddingtonLastNameQuery = """
UPDATE Users
SET last_name = 'Reddington'
WHERE user_id = (
    SELECT r.user_id
    FROM Reservation r
    WHERE r.status = 'cancelled'
    GROUP BY r.user_id
    HAVING COUNT(r.reservation_id) = (
        SELECT MAX(temp.cxl_count)
        FROM (
            SELECT COUNT(r2.reservation_id) AS cxl_count
            FROM Reservation r2
            WHERE r2.status = 'cancelled'
            GROUP BY r2.user_id
        ) temp
    )
);
"""

#حذف رزروهای لغوشدهٔ کاربر با نام خانوادگی Reddington
SportTicket_DeleteReddingtonCancelledReservationsQuery = """
DELETE FROM Reservation
WHERE status = 'cancelled'
  AND user_id IN (
      SELECT user_id
      FROM Users
      WHERE last_name = 'Reddington'
  );
"""

#حذف تمام رزروهای لغوشده از سامانه
SportTicket_DeleteAllCancelledReservationsQuery = """
DELETE FROM Reservation
WHERE status = 'cancelled';
"""

#اعمال ۱۰ درصد تخفیف برای مسابقات ورزشگاه آزادی در یک تاریخ مشخص
SportTicket_AzadiStadiumDiscountQuery = """
UPDATE Event
SET ticket_price = ticket_price * 0.90
WHERE venue_id IN (
    SELECT venue_id
    FROM Venue
    WHERE name = 'ورزشگاه آزادی'
)
AND event_date >= '2026-08-10 00:00:00'
AND event_date <= '2026-08-10 23:59:59';
"""

#نمایش موضوع و تعداد گزارش‌ها برای مسابقه‌ای با بیشترین گزارش
SportTicket_MostReportedEventSubjectsQuery = """
SELECT rep.subject, COUNT(rep.report_id) AS report_count
FROM Report rep
WHERE rep.event_id = (
    SELECT r.event_id
    FROM Report r
    GROUP BY r.event_id
    HAVING COUNT(r.report_id) = (
        SELECT MAX(temp.rep_count)
        FROM (
            SELECT COUNT(r2.report_id) AS rep_count
            FROM Report r2
            GROUP BY r2.event_id
        ) temp
    )
)
GROUP BY rep.subject;
"""