data_devolucao = """
    CREATE PROCEDURE IF NOT EXISTS calcular_data_devolucao(OUT data_devolucao DATE)
    BEGIN
        DECLARE dia_semana INT;

        SET data_devolucao = DATE_ADD(CURDATE(), INTERVAL 15 DAY);

        SET dia_semana = DAYOFWEEK(data_devolucao);

        IF dia_semana = 1 THEN
            SET data_devolucao = DATE_ADD(data_devolucao, INTERVAL 1 DAY);
        ELSEIF dia_semana = 7 THEN
            SET data_devolucao = DATE_ADD(data_devolucao, INTERVAL 2 DAY);
        END IF;
    END;
"""