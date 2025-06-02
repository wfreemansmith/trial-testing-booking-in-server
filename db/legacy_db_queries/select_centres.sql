SELECT
	PretestCentreNumber AS centre_id,
	LiveCentreNumber AS live_centre_number,
	Name AS 'centre_name',
	NULLIF(Partner, 'None') AS 'partner',
	Address1 AS 'address_1',
	Address2 AS 'address_2',
	Address3 AS 'address_3',
	Address4 AS 'address_4',
	Address5 AS 'address_5',
	CountryID AS 'country_id',
	ContactTelNo1 AS 'phone_number'
FROM Pretesting.dbo.tblCentre
WHERE Name IS NOT NULL;