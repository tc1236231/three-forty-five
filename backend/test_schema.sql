DROP TABLE IF EXISTS hil_att;
CREATE TABLE hil_att (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sli_no INTEGER NOT NULL,
    paid_amt REAL,
    order_no INTEGER NOT NULL,
    price_type_desc TEXT,
    price_type_short_desc TEXT,
    sli_status_desc TEXT,
    perf_dt TEXT,
    order_dt TEXT,
    price_type_category_desc TEXT,
    price_type_category_short_desc TEXT,
    perf_desc TEXT,
    prod_desc TEXT,
    perf_type_desc TEXT,
    season_desc TEXT,
    season_fy INTEGER,
    mos_desc TEXT,
    site_code TEXT,
    gl_account_no TEXT
    );