-- Dodawanie rekordu do tabeli "city" pkt
CREATE PROCEDURE DodajMiasto(IN nazwaMiasta VARCHAR(255))
BEGIN
    INSERT INTO city (name) VALUES (nazwaMiasta);
END;

CALL DodajMiasto('Kaktus');

-- Dodawanie rekordu do tabeli "historical_weather"
CREATE PROCEDURE DodajHistoricalWeather(
    IN data DATE,
    IN tempSrednia DECIMAL(5,2),
    IN tempMin DECIMAL(5,2),
    IN tempMax DECIMAL(5,2),
    IN kierunekWiatru FLOAT,
    IN predkoscWiatru DECIMAL(5,2),
    IN cisnienie INT,
    IN miastoID INT
)
BEGIN
    INSERT INTO historical_weather (w_date, temp_avg, temp_min, temp_max, wind_dir, wind_speed, pressure, city)
    VALUES (data, tempSrednia, tempMin, tempMax, kierunekWiatru, predkoscWiatru, cisnienie, miastoID);
END;

CALL DodajHistoricalWeather('2024-01-14', 25.5, 20.0, 30.0, 119.0, 15.0, 1012, 1);

-- Aktualizacja rekordu w tabeli "city"
CREATE PROCEDURE AktualizujMiasto(IN miastoID INT, IN nowaNazwa VARCHAR(255))
BEGIN
    UPDATE city SET name = nowaNazwa WHERE ID = miastoID;
END;

CALL AktualizujMiasto(117, 'NowaNazwaMiasta');

-- Usuwanie rekordu z tabeli "historical_weather"
CREATE PROCEDURE UsunHistoricalWeather(IN rekordID INT)
BEGIN
    DELETE FROM historical_weather WHERE ID = rekordID;
END;

-- Procedura logowania informacji do tabeli
CREATE PROCEDURE LogujInformacje(IN komunikat VARCHAR(255))
BEGIN
    INSERT INTO log_table (message) VALUES (komunikat);
END;

CALL LogujInformacje('Dodano nowy rekord do tabeli.');

-- Procedura sprawdzająca istnienie miasta
CREATE PROCEDURE SprawdzIstnienieMiasta(IN miastoID INT)
BEGIN
    DECLARE miastoNieIstnieje BOOLEAN DEFAULT FALSE;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET miastoNieIstnieje = TRUE;

    SELECT * FROM city WHERE ID = miastoID;

    IF miastoNieIstnieje THEN
        SELECT 'Miasto o podanym ID nie istnieje' AS Komunikat;
    END IF;
END;

CALL SprawdzIstnienieMiasta(1234);

-- Procedura dodająca rekord do tabeli historical_weather z możliwością pominięcia niektórych parametrów
CREATE PROCEDURE DodajHistoricalWeatherZParametrami(
    IN data DATE,
    IN tempSrednia DECIMAL(5,2),
    IN tempMin DECIMAL(5,2),
    IN tempMax DECIMAL(5,2),
    IN kierunekWiatru FLOAT,
    IN predkoscWiatru DECIMAL(5,2),
    IN cisnienie INT,
    IN miastoID INT
)
BEGIN
    INSERT INTO historical_weather (w_date, temp_avg, temp_min, temp_max, wind_dir, wind_speed, pressure, city)
    VALUES (data, tempSrednia, tempMin, tempMax, kierunekWiatru, predkoscWiatru, cisnienie, miastoID);
END;

CALL DodajHistoricalWeatherZParametrami('2024-01-15', 22.0, NULL, NULL, 12.0, NULL, NULL, 118);

-- Funkcja konwertująca temperaturę z Celsiusza na Fahrenheita
CREATE FUNCTION KonwertujNaFahrenheita(tempCelsius DECIMAL(5,2)) RETURNS DECIMAL(5,2)
BEGIN
    DECLARE tempFahrenheit DECIMAL(5,2);
    SET tempFahrenheit = (tempCelsius * 9 / 5) + 32;
    RETURN tempFahrenheit;
END;

SELECT KonwertujNaFahrenheita(25.5) AS TempFahrenheit;

-- Trigger zmieniający kierunek wiatru dla temperatury poniżej 10 stopni
DELIMITER //
CREATE TRIGGER ZimnyMiesiacTrigger
BEFORE INSERT ON historical_weather
FOR EACH ROW
BEGIN
    IF NEW.temp_avg < 10.0 THEN
        SET NEW.wind_dir = 123.45;
    END IF;
END;
//
DELIMITER ;

INSERT INTO historical_weather (w_date, temp_avg, temp_min, temp_max, wind_dir, wind_speed, pressure, city) VALUES ('2015-01-01', 8.5, 5.0, 12.0, 45.67, 10.0, 1015, 1);