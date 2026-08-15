export const mockMatches = [
  {
    event_id: 1,
    event_datetime: "2026-08-20T18:30:00",
    event_status: "scheduled",

    sport_id: 1,
    sport_name: "فوتبال",

    league_id: 1,
    league_name: "لیگ برتر",
    league_season: "1405-1406",

    venue_id: 1,
    venue_name: "ورزشگاه آزادی",
    venue_address: "تهران، مجموعه ورزشی آزادی",
    venue_capacity: 78000,

    city_id: 1,
    city_name: "تهران",

    province_id: 1,
    province_name: "تهران",

    country_id: 1,
    country_name: "ایران",
    country_iso_code: "IR",

    home_team_id: 1,
    home_team_name: "استقلال",
    home_team_logo_url: "/images/teams/esteghlal.png",

    away_team_id: 2,
    away_team_name: "پرسپولیس",
    away_team_logo_url: "/images/teams/persepolis.png",

    ticket_category_id: 1,
    ticket_category_name: "جایگاه ویژه",

    current_price: 850000,

    sales_start_at: "2026-08-10T10:00:00",
    sales_end_at: "2026-08-20T17:30:00",

    section_id: 1,
    section_name: "جایگاه ویژه",
    section_capacity: 500,
    section_type_id: 1,
    section_type_name: "VIP",

    available_count: 120,
  },

  {
    event_id: 2,
    event_datetime: "2026-08-22T20:00:00",
    event_status: "scheduled",

    sport_id: 1,
    sport_name: "فوتبال",

    league_id: 1,
    league_name: "لیگ برتر",
    league_season: "1405-1406",

    venue_id: 2,
    venue_name: "ورزشگاه نقش جهان",
    venue_address: "اصفهان، بلوار کشاورز",
    venue_capacity: 75000,

    city_id: 2,
    city_name: "اصفهان",

    province_id: 2,
    province_name: "اصفهان",

    country_id: 1,
    country_name: "ایران",
    country_iso_code: "IR",

    home_team_id: 3,
    home_team_name: "سپاهان",
    home_team_logo_url: "/images/teams/sepahan.png",

    away_team_id: 4,
    away_team_name: "تراکتور",
    away_team_logo_url: "/images/teams/tractor.png",

    ticket_category_id: 2,
    ticket_category_name: "جایگاه عادی",

    current_price: 450000,

    sales_start_at: "2026-08-12T09:00:00",
    sales_end_at: "2026-08-22T19:00:00",

    section_id: 2,
    section_name: "جایگاه عادی",
    section_capacity: 2000,
    section_type_id: 2,
    section_type_name: "Normal",

    available_count: 850,
  },

  {
    event_id: 3,
    event_datetime: "2026-08-25T17:00:00",
    event_status: "scheduled",

    sport_id: 2,
    sport_name: "بسکتبال",

    league_id: 2,
    league_name: "لیگ برتر بسکتبال",
    league_season: "1405",

    venue_id: 3,
    venue_name: "سالن آزادی",
    venue_address: "تهران، مجموعه ورزشی آزادی",
    venue_capacity: 12000,

    city_id: 1,
    city_name: "تهران",

    province_id: 1,
    province_name: "تهران",

    country_id: 1,
    country_name: "ایران",
    country_iso_code: "IR",

    home_team_id: 5,
    home_team_name: "شهرداری گرگان",
    home_team_logo_url: "/images/teams/gorgan.png",

    away_team_id: 6,
    away_team_name: "ذوب آهن",
    away_team_logo_url: "/images/teams/zobahan.png",

    ticket_category_id: 3,
    ticket_category_name: "ورودی عادی",

    current_price: 250000,

    sales_start_at: "2026-08-15T10:00:00",
    sales_end_at: "2026-08-25T16:00:00",

    section_id: 3,
    section_name: "جایگاه اصلی",
    section_capacity: 800,
    section_type_id: 2,
    section_type_name: "Normal",

    available_count: 340,
  },

  {
    event_id: 4,
    event_datetime: "2026-08-27T19:30:00",
    event_status: "scheduled",

    sport_id: 3,
    sport_name: "والیبال",

    league_id: 3,
    league_name: "لیگ برتر والیبال",
    league_season: "1405",

    venue_id: 4,
    venue_name: "سالن دوازده هزار نفری آزادی",
    venue_address: "تهران، مجموعه ورزشی آزادی",
    venue_capacity: 12000,

    city_id: 1,
    city_name: "تهران",

    province_id: 1,
    province_name: "تهران",

    country_id: 1,
    country_name: "ایران",
    country_iso_code: "IR",

    home_team_id: 7,
    home_team_name: "پیکان",
    home_team_logo_url: "/images/teams/peikan.png",

    away_team_id: 8,
    away_team_name: "شهداب یزد",
    away_team_logo_url: "/images/teams/shahdab.png",

    ticket_category_id: 4,
    ticket_category_name: "جایگاه ویژه",

    current_price: 300000,

    sales_start_at: "2026-08-16T12:00:00",
    sales_end_at: "2026-08-27T18:30:00",

    section_id: 4,
    section_name: "جایگاه ویژه",
    section_capacity: 600,
    section_type_id: 1,
    section_type_name: "VIP",

    available_count: 75,
  },
];

export const mockFilters = {
  sports: [
    { id: 1, name: "فوتبال" },
    { id: 2, name: "بسکتبال" },
    { id: 3, name: "والیبال" },
  ],

  teams: [
    { id: 1, name: "استقلال" },
    { id: 2, name: "پرسپولیس" },
    { id: 3, name: "سپاهان" },
    { id: 4, name: "تراکتور" },
    { id: 5, name: "شهرداری گرگان" },
    { id: 6, name: "ذوب آهن" },
    { id: 7, name: "پیکان" },
    { id: 8, name: "شهداب یزد" },
  ],

  cities: [
    { id: 1, name: "تهران" },
    { id: 2, name: "اصفهان" },
  ],

  venues: [
    { id: 1, name: "ورزشگاه آزادی" },
    { id: 2, name: "ورزشگاه نقش جهان" },
    { id: 3, name: "سالن آزادی" },
    { id: 4, name: "سالن دوازده هزار نفری آزادی" },
  ],

  ticketCategories: [
    { id: 1, name: "جایگاه ویژه" },
    { id: 2, name: "جایگاه عادی" },
    { id: 3, name: "ورودی عادی" },
    { id: 4, name: "جایگاه ویژه" },
  ],
};

export const mockReservations = [
  {
    reservation_id: 12456789,
    event_id: 1,
    event_datetime: "2026-09-09T18:00:00Z",
    home_team_name: "استقلال",
    away_team_name: "پرسپولیس",
    venue_name: "ورزشگاه آزادی",
    city_name: "تهران",

    ticket_category_id: 1,
    ticket_category_name: "VIP",

    status: "paid",
    quantity: 1,
    price: 500000,
    total_amount: 500000,

    reserved_at: "2026-08-15T12:30:00Z",
    expires_at: null,
    paid_at: "2026-08-15T12:35:20Z",
    remaining_seconds: null,

    seats: [
      {
        inventory_id: 101,
        seat_id: 501,
        row_number: "5",
        seat_number: 24,
        section_id: 1,
        section_name: "VIP",
      },
    ],
  },

  {
    reservation_id: 12456790,
    event_id: 2,
    event_datetime: "2026-09-10T20:30:00Z",
    home_team_name: "سپاهان",
    away_team_name: "تراکتور",
    venue_name: "ورزشگاه نقش جهان",
    city_name: "اصفهان",

    ticket_category_id: 2,
    ticket_category_name: "Premium",

    status: "pending",
    quantity: 1,
    price: 480000,
    total_amount: 480000,

    reserved_at: "2026-08-15T16:45:00Z",
    expires_at: "2026-08-15T17:00:00Z",
    paid_at: null,
    remaining_seconds: 382,

    seats: [
      {
        inventory_id: 102,
        seat_id: 602,
        row_number: "7",
        seat_number: 15,
        section_id: 2,
        section_name: "Premium",
      },
    ],
  },

  {
    reservation_id: 12456791,
    event_id: 3,
    event_datetime: "2026-09-12T17:00:00Z",
    home_team_name: "بارسلونا",
    away_team_name: "رئال مادرید",
    venue_name: "ورزشگاه نیوکمپ",
    city_name: "بارسلونا",

    ticket_category_id: 3,
    ticket_category_name: "Normal",

    status: "paid",
    quantity: 2,
    price: 300000,
    total_amount: 600000,

    reserved_at: "2026-08-10T10:20:00Z",
    expires_at: null,
    paid_at: "2026-08-10T10:25:10Z",
    remaining_seconds: null,

    seats: [
      {
        inventory_id: 103,
        seat_id: 701,
        row_number: "12",
        seat_number: 18,
        section_id: 3,
        section_name: "Normal",
      },
      {
        inventory_id: 104,
        seat_id: 702,
        row_number: "12",
        seat_number: 19,
        section_id: 3,
        section_name: "Normal",
      },
    ],
  },

  {
    reservation_id: 12456792,
    event_id: 4,
    event_datetime: "2026-09-15T19:30:00Z",
    home_team_name: "پیکان",
    away_team_name: "سایپا",
    venue_name: "ورزشگاه دستگردی",
    city_name: "تهران",

    ticket_category_id: 4,
    ticket_category_name: "Economy",

    status: "expired",
    quantity: 1,
    price: 180000,
    total_amount: 180000,

    reserved_at: "2026-08-12T14:00:00Z",
    expires_at: "2026-08-12T14:15:00Z",
    paid_at: null,
    remaining_seconds: 0,

    seats: [
      {
        inventory_id: 105,
        seat_id: 801,
        row_number: "3",
        seat_number: 8,
        section_id: 4,
        section_name: "Economy",
      },
    ],
  },

  {
    reservation_id: 12456793,
    event_id: 5,
    event_datetime: "2026-09-18T18:00:00Z",
    home_team_name: "ذوب آهن",
    away_team_name: "فولاد",
    venue_name: "ورزشگاه فولادشهر",
    city_name: "اصفهان",

    ticket_category_id: 2,
    ticket_category_name: "Premium",

    status: "cancelled",
    quantity: 1,
    price: 350000,
    total_amount: 350000,

    reserved_at: "2026-08-05T11:00:00Z",
    expires_at: null,
    paid_at: null,
    remaining_seconds: null,

    seats: [
      {
        inventory_id: 106,
        seat_id: 901,
        row_number: "9",
        seat_number: 31,
        section_id: 2,
        section_name: "Premium",
      },
    ],
  },
];

export const mockReports = [
  {
    report_id: 15,
    user_id: 1,
    ticket_id: 123,
    reservation_id: 45,
    issue_type: "seat_problem",
    message: "شماره صندلی نمایش داده شده با صندلی انتخابی من مطابقت ندارد.",
    status: "in_review",
  },
  {
    report_id: 14,
    user_id: 1,
    ticket_id: null,
    reservation_id: 44,
    issue_type: "payment_problem",
    message: "مبلغ پرداختی از حساب من کسر شده اما وضعیت رزرو هنوز پرداخت نشده است.",
    status: "pending",
  },
  {
    report_id: 13,
    user_id: 1,
    ticket_id: 120,
    reservation_id: 43,
    issue_type: "ticket_information",
    message: "اطلاعات درج شده روی بلیط با اطلاعات مسابقه مطابقت ندارد.",
    status: "resolved",
  },
  {
    report_id: 12,
    user_id: 1,
    ticket_id: null,
    reservation_id: 42,
    issue_type: "pricing_problem",
    message: "قیمت نهایی بلیط با مبلغی که هنگام انتخاب بلیط نمایش داده شد متفاوت است.",
    status: "rejected",
  },
  {
    report_id: 11,
    user_id: 1,
    ticket_id: 118,
    reservation_id: 40,
    issue_type: "venue_problem",
    message: "آدرس ورزشگاه نمایش داده شده در اطلاعات بلیط اشتباه است.",
    status: "pending",
  },
];

export const mockSupportReservations = [
  {
    reservation_id: 101,

    user_id: 12,
    first_name: "زهرا",
    last_name: "احمدی",
    email: "zahra@example.com",
    phone: "09123456789",

    event_id: 1,
    event_datetime: "2026-09-05T18:30:00Z",
    home_team_name: "پرسپولیس",
    away_team_name: "استقلال",

    reservation_status: "pending",
    support_review_status: "unreviewed",
    support_note: null,

    reserved_at: "2026-08-15T14:20:00Z",
    expires_at: "2026-08-15T14:35:00Z",
    paid_at: null,

    total_amount: 1200000,

    support_reviewed_by: null,
    support_reviewed_at: null,

    inventory_id: 501,
    row_number: "12",
    seat_number: 18,
    section_name: "VIP",

    ticket_id: null,
    ticket_status: null,
  },

  {
    reservation_id: 102,

    user_id: 15,
    first_name: "محمد",
    last_name: "رضایی",
    email: "mohammad@example.com",
    phone: "09121234567",

    event_id: 2,
    event_datetime: "2026-09-10T20:00:00Z",
    home_team_name: "شهرداری ارومیه",
    away_team_name: "پیکان تهران",

    reservation_status: "paid",
    support_review_status: "approved",
    support_note: "رزرو بررسی و تأیید شد.",

    reserved_at: "2026-08-14T10:15:00Z",
    expires_at: null,
    paid_at: "2026-08-14T10:18:32Z",

    total_amount: 800000,

    support_reviewed_by: 3,
    support_reviewed_at: "2026-08-14T10:20:00Z",

    inventory_id: 502,
    row_number: "8",
    seat_number: 24,
    section_name: "Premium",

    ticket_id: 750,
    ticket_status: "issued",
  },

  {
    reservation_id: 103,

    user_id: 21,
    first_name: "علی",
    last_name: "کریمی",
    email: "ali@example.com",
    phone: "09351234567",

    event_id: 3,
    event_datetime: "2026-09-15T17:00:00Z",
    home_team_name: "تراکتور",
    away_team_name: "سپاهان",

    reservation_status: "cancelled",
    support_review_status: "cancelled",
    support_note: "رزرو به درخواست کاربر لغو شد.",

    reserved_at: "2026-08-13T16:10:00Z",
    expires_at: null,
    paid_at: null,

    total_amount: 600000,

    support_reviewed_by: 4,
    support_reviewed_at: "2026-08-13T16:20:00Z",

    inventory_id: 503,
    row_number: "5",
    seat_number: 11,
    section_name: "Normal",

    ticket_id: null,
    ticket_status: null,
  },

  {
    reservation_id: 104,

    user_id: 27,
    first_name: "سارا",
    last_name: "محمدی",
    email: "sara@example.com",
    phone: "09199887766",

    event_id: 4,
    event_datetime: "2026-09-20T19:30:00Z",
    home_team_name: "استقلال",
    away_team_name: "گل‌گهر",

    reservation_status: "pending",
    support_review_status: "modified",
    support_note: "مهلت رزرو توسط پشتیبان تمدید شد.",

    reserved_at: "2026-08-15T15:00:00Z",
    expires_at: "2026-08-15T16:00:00Z",
    paid_at: null,

    total_amount: 500000,

    support_reviewed_by: 3,
    support_reviewed_at: "2026-08-15T15:10:00Z",

    inventory_id: 504,
    row_number: "15",
    seat_number: 7,
    section_name: "Economy",

    ticket_id: null,
    ticket_status: null,
  },
];