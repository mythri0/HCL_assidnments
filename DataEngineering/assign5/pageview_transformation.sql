SELECT *
FROM `learned-stone-513710-r3.website_analytics.external_pageviews`;

CREATE TABLE
  `learned-stone-513710-r3.website_analytics.pageview_summary`
AS
SELECT
  page_url,
  COUNT(*) AS total_pageviews,
  COUNT(DISTINCT user_id) AS unique_users
FROM
  `learned-stone-513710-r3.website_analytics.external_pageviews`
GROUP BY
  page_url;