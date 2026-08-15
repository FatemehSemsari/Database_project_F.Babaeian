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