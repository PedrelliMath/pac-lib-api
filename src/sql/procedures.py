emprestimo_status_procedure = """
    CREATE PROCEDURE check_situacao(IN emprestimo_id INT, OUT result BOOLEAN)
    BEGIN
        DECLARE data_devolucao TIMESTAMP;

        SELECT data_devolucao INTO data_devolucao FROM emprestimo WHERE id = emprestimo_id;

        IF CURRENT_TIMESTAMP() <= data_devolucao THEN
            SET result = TRUE;
        ELSE
            SET result = FALSE;
        END IF;
    END;
"""