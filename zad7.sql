
-- Procedura generująca zestawienie miesięczne dla średnich temperatur
DELIMITER //
CREATE PROCEDURE GenerujZestawienieMiesieczne(IN miastoID INT)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'summary_monthly' AND table_schema = DATABASE()) THEN
        CREATE TABLE summary_monthly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_id INT,
            month INT,
            average_temperature DECIMAL(5,2),
            UNIQUE KEY unique_monthly (city_id, month)
        );
    END IF;

    INSERT INTO summary_monthly (city_id, month, average_temperature)
    SELECT
        miastoID AS city_id,
        MONTH(w_date) AS month,
        AVG(temp_avg) AS average_temperature
    FROM historical_weather
    WHERE city = miastoID
    GROUP BY month;
END //
CALL GenerujZestawienieMiesieczne(1);
DELIMITER ;

-- Procedura generująca zestawienie roczne dla średnich temperatur w danym roku
DELIMITER //
CREATE PROCEDURE GenerujZestawienieRok(IN miastoID INT, IN rok INT)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'summary_yearly' AND table_schema = DATABASE()) THEN
        CREATE TABLE summary_yearly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_id INT,
            month INT,
            average_temperature DECIMAL(5,2),
            max_temperature DECIMAL(5,2),
            min_temperature DECIMAL(5,2),
            UNIQUE KEY unique_yearly (city_id, month)
        );
    END IF;

    INSERT INTO summary_yearly (city_id, month, average_temperature, max_temperature, min_temperature)
    SELECT
        miastoID AS city_id,
        EXTRACT(MONTH FROM w_date) AS month,
        AVG(temp_avg) AS average_temperature,
        MAX(temp_max) AS max_temperature,
        MIN(temp_min) AS min_temperature
    FROM historical_weather
    WHERE city = miastoID AND EXTRACT(YEAR FROM w_date) = rok
    GROUP BY month;
END //
DELIMITER ;
CALL GenerujZestawienieRok(1,2023);

-- Funkcja sprawdzająca, czy dany miesiąc jest chłodny
CREATE FUNCTION CzyChlodnyMiesiac(sredniaTemperatura DECIMAL(5,2)) RETURNS BOOLEAN
BEGIN
    DECLARE chlodny BOOLEAN;

    SET chlodny = (sredniaTemperatura < 10.0);

    RETURN chlodny;
END;

SELECT CzyChlodnyMiesiac(12) AS 'Czy Chłodny Miesiąc?';

-- Funkcja zwracająca liczbę rekordów w tabeli historical_weather
CREATE FUNCTION IloscRekordowHistoricalWeather() RETURNS INT
BEGIN
    DECLARE ilosc INT;

    SELECT COUNT(*) INTO ilosc FROM historical_weather;

    RETURN ilosc;
END;

SELECT IloscRekordowHistoricalWeather() AS 'Liczba Rekordów w Historical Weather';
