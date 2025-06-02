WITH unpivoted AS (
  SELECT PretestCentreNumber AS centre_id, ContactName1 AS contact_name, ContactEmail1 AS contact_email
  FROM Pretesting.dbo.tblCentre
  WHERE ContactEmail1 IS NOT NULL

  UNION ALL

  SELECT PretestCentreNumber AS centre_id, ContactName2 AS contact_name, ContactEmail2 AS contact_email
  FROM Pretesting.dbo.tblCentre
  WHERE ContactEmail2 IS NOT NULL
),
split_contacts AS (
  SELECT 
    u.centre_id,
    LTRIM(RTRIM(u.contact_name)) AS contact_name,
    LTRIM(RTRIM(value)) AS contact_email
  FROM unpivoted u
  CROSS APPLY STRING_SPLIT(u.contact_email, ';')
),
numbered_contacts AS (
  SELECT 
    centre_id,
    contact_name,
    contact_email,
    ROW_NUMBER() OVER (PARTITION BY centre_id ORDER BY (SELECT NULL)) AS rn
  FROM split_contacts
  WHERE contact_email <> ''
)
SELECT
  centre_id,
  contact_name,
  contact_email,
  CASE WHEN rn = 1 THEN 'TRUE' ELSE 'FALSE' END AS primary_contact
FROM numbered_contacts
ORDER BY centre_id, rn;
