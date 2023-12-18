# House Listing Web Scrape Project

## Overview
The House Listing Web Scrape Project involves gathering information from the Rumah123 website by scraping data from approximately 80,000 house listings in Bekasi, Indonesia. The collected data will then be imported into a database, ensuring proper normalization for efficient storage and retrieval. The normalization process aims to organize the data in a structured manner, reducing redundancy and improving overall database efficiency. Once the data is successfully imported, the project will involve querying and analyzing the information within the database. This step will enable the extraction of meaningful insights, trends, and patterns from the gathered house listing data. The ultimate goal of the project is to provide a well-organized and analyzable dataset, facilitating further exploration and understanding of the housing market represented by the Rumah123 website.

## The Methodology
![](/assets/rumah123_flowchart.jpg)
The project methodology involves a systematic four-step process. First, in the extraction phase, data is retrieved from the Rumah123 website, encompassing various locations from `locations.txt`. This is achieved using Scrapy as the web scraper, allowing us to navigate through the website's structure and collect relevant information. Additionally, Playwright is employed to handle JavaScript-rendered content, ensuring a comprehensive data extraction process.

Moving on to the transformation stage, the collected data undergoes cleaning procedures using Jupyter Notebook. This step focuses on enhancing the data's quality and consistency, making it suitable for further analysis. By addressing inconsistencies and outliers, we ensure that the dataset is well-prepared for meaningful insights.

The third step, loading the cleaned and transformed data into a database is a pivotal stage in our methodology. We design the database schema, emphasizing normalization techniques to optimize storage and retrieval efficiency. The PostgreSQL database, hosted on the ElephantSQL service, serves as the repository for our organized and refined dataset. This structured approach facilitates seamless integration and accessibility for subsequent analysis.

![](/assets/database_schema.png)

The final stage involves querying the PostgreSQL database for insightful analysis. Utilizing Jupyter Notebook and a Streamlit app, we execute queries to extract valuable information, trends, and patterns from the dataset. This interactive and user-friendly approach allows for a comprehensive exploration of the housing market data, empowering users to make informed decisions based on the queried insights.

## Answering Questions

### Can you give me the list of 10 houses with my specified criteria?
- house properties
- under one billion rupiah
- 3 or more beds and bathrooms
- one garage
- located on tambun_selatan
- sorted by the cheapest price while maximizing the number of bedrooms.
```SQL
SELECT
    property.id,
    property.price AS price_in_million_idr,
    property.bedroom_count,
    property.bathroom_count,
    property.garage_count,
    property.listing_description,
    property."LT",
    property."LB",
    location."name" AS location_name
FROM 
    "public"."property_listing" property
JOIN
    "public"."location" location
ON 
    property.location_id = location.id
WHERE
    bedroom_count >= 3 
    AND bathroom_count >= 3
    AND garage_count = 1
    AND price <= 1000 
    AND location_id = (SELECT id FROM "public"."location" WHERE name = 'Tambun Selatan, Bekasi')
    AND property_type_id = (SELECT id FROM "property_type" WHERE "name" = 'Rumah')
    ORDER BY price ASC,  bedroom_count DESC
    LIMIT 10;
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>price_in_million_idr</th>
      <th>bedroom_count</th>
      <th>bathroom_count</th>
      <th>garage_count</th>
      <th>listing_description</th>
      <th>LT</th>
      <th>LB</th>
      <th>location_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7349</td>
      <td>500</td>
      <td>5</td>
      <td>3</td>
      <td>1</td>
      <td>Rumah Hook Griya Asri 2 Siap Huni Strategis Akses Tol Baru</td>
      <td>132</td>
      <td>250</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>1</th>
      <td>9491</td>
      <td>550</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>Dijual murah, Rumah 120m² di Taman Tridaya Indah Tambun Bekasi</td>
      <td>120</td>
      <td>100</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4261</td>
      <td>650</td>
      <td>5</td>
      <td>3</td>
      <td>1</td>
      <td>Dijual Rumah Murah Dan Nyaman di Villa Bekasi Indah Daerah Tambun ...</td>
      <td>110</td>
      <td>110</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18314</td>
      <td>650</td>
      <td>5</td>
      <td>3</td>
      <td>1</td>
      <td>Jual rumah 2 lantai super murah di tambun selatan</td>
      <td>132</td>
      <td>250</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>879</td>
      <td>650</td>
      <td>4</td>
      <td>4</td>
      <td>1</td>
      <td>Rumah murah minimalis siap huni</td>
      <td>120</td>
      <td>160</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>5</th>
      <td>18932</td>
      <td>650</td>
      <td>4</td>
      <td>4</td>
      <td>1</td>
      <td>Rumah cantik minimalis siap huni</td>
      <td>120</td>
      <td>160</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>6</th>
      <td>15871</td>
      <td>750</td>
      <td>8</td>
      <td>8</td>
      <td>1</td>
      <td>Dijual Cepat Kontrakan 8 Pintu Siap Huni di Tambun, Bekasi</td>
      <td>270</td>
      <td>185</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>7</th>
      <td>15870</td>
      <td>750</td>
      <td>8</td>
      <td>8</td>
      <td>1</td>
      <td>Dijual Cepat Kontrakan 8 Pintu Siap Huni di Tambun, Bekasi</td>
      <td>270</td>
      <td>185</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>8</th>
      <td>15260</td>
      <td>825</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>Rumah di sumber Jaya tambun kab bekasi depan lapangan dan masjid</td>
      <td>135</td>
      <td>135</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
    <tr>
      <th>9</th>
      <td>4255</td>
      <td>850</td>
      <td>4</td>
      <td>3</td>
      <td>1</td>
      <td>Dijual rumah siap huni di daerah sekitar Tambun Selatan Bekasi</td>
      <td>136</td>
      <td>145</td>
      <td>Tambun Selatan, Bekasi</td>
    </tr>
  </tbody>
</table>
</div>

### Where is the cheapest location to buy land property?

```SQL
SELECT
    (SELECT name FROM "public"."location" WHERE id = location_id),
    COUNT(*)
FROM
    (
    SELECT
    *
    FROM 
        "public"."property_listing"
    WHERE
        property_type_id = (SELECT id FROM property_type WHERE name = 'Tanah')
    ORDER BY 
        price ASC
    LIMIT 100
    ) as subquery
GROUP BY
    subquery.location_id
ORDER BY
    count DESC
LIMIT 5;
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Cikarang, Bekasi</td>
      <td>23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Tambun Selatan, Bekasi</td>
      <td>7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Jatisampurna, Bekasi</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Bekasi Timur, Bekasi</td>
      <td>6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Cibitung, Bekasi</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>

### Can you give me the unique count of property listings, agents, locations, users, and property type in the database?
```SQL
SELECT
    'public.user' AS table_name,
    COUNT(*) AS row_count
FROM
    "public"."user"

UNION

SELECT
    'public.agent_corporate' AS table_name,
    COUNT(*) AS row_count
FROM
    "public"."agent_corporate"

UNION

SELECT
    'public.property_listing' AS table_name,
    COUNT(*) AS row_count
FROM
    "public"."property_listing"
    
UNION

SELECT
    'public.location' AS table_name,
    COUNT(*) AS row_count
FROM
    "public"."location"

UNION

SELECT
    'public.property_type' AS table_name,
    COUNT(*) AS row_count
FROM
    "public"."property_type"
    
UNION

SELECT
    'public.listing_type' AS table_name,
    COUNT(*) AS row_count
FROM
    "public"."listing_type";
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>table_name</th>
      <th>row_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>public.listing_type</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>public.location</td>
      <td>86</td>
    </tr>
    <tr>
      <th>2</th>
      <td>public.property_listing</td>
      <td>79192</td>
    </tr>
    <tr>
      <th>3</th>
      <td>public.user</td>
      <td>4313</td>
    </tr>
    <tr>
      <th>4</th>
      <td>public.agent_corporate</td>
      <td>877</td>
    </tr>
    <tr>
      <th>5</th>
      <td>public.property_type</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>

## Getting Started
### Install Packages
```
scrapy
scrapy-playwright
streamlit
psycopg2
pandas
```

### Web Scraping
#### Create Scrapy Project
```cmd
scrapy startproject [project_name]
or
scrapy startproject rumah123
```
#### Copy Rumah123Spider
```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you put your spiders
            __init__.py
            [rumah123_spider.py] <------ Put your spider here
```

#### Modify Settings.py
Add user agent to simulate user behaviour and AutoThrottle to manage requests.
```python
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

# Enable and configure the AutoThrottle extension
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True
```
#### Run Spider
```
scrapy crawl [project_name] -o [filename].csv
or
scrapy crawl rumah123 -o rumah123_data.csv
```

### Import dataset into PostgreSQL
#### Create database instance on ElephantSQL
https://www.elephantsql.com/
#### Modify connection variables
Head into `postgres_csv_uploader.py` go into the main() function. Add your database information and your CSV file path.

```python
hostname = "YOUR HOST HERE"
username = "YOUR USERNAME HERE"
password = "YOUR DATABASE PASSWORD HERE"
# Default port for postgreSQL
port_id = "5432" 

file_path = 'YOUR CSV PATH HERE'
```
#### Run the script
```cmd
python postgres_csv_uploader.py
```
