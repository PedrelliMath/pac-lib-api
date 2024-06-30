emprestimo_status_trigger = """
    CREATE TRIGGER before_insert_emprestimo
    BEFORE INSERT ON emprestimo
    FOR EACH ROW
    BEGIN
        CALL check_situacao(NEW.id);
    END;
"""