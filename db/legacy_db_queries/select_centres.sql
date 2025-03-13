SELECT
	CONCAT('"', PretestCentreNumber, '"') AS centre_id,
	LiveCentreNumber AS live_centre_number,
	Name AS 'centre_name',
	Address1 AS 'address_1',
	Address2 AS 'address_2',
	Address3 AS 'address_3',
	Address4 AS 'address_4',
	Address5 AS 'address_5',
	CountryID AS 'country_id',
	ContactTelNo1 AS 'phone_number',
	ContactName1 AS 'primary_contact_name',
	ContactEmail1 AS 'primary_contact_email',
	ContactName2 AS 'secondary_contact_name',
	ContactEmail2 AS 'secondary_contact_email'
FROM Pretesting.dbo.tblCentre;