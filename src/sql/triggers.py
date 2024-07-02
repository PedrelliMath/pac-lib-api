incremente_exemplar = """
    CREATE TRIGGER IF NOT EXISTS incrementar_quantidade_exemplares
    AFTER INSERT ON exemplares
    FOR EACH ROW
    BEGIN
        UPDATE livro
        SET quantidade_exemplares = quantidade_exemplares + 1
        WHERE id = NEW.livro_id;
    END;
"""

decrementa_exemplar = """
    CREATE TRIGGER IF NOT EXISTS decrementar_quantidade_exemplares
    AFTER DELETE ON exemplares
    FOR EACH ROW
    BEGIN
        UPDATE livro
        SET quantidade_exemplares = quantidade_exemplares - 1
        WHERE id = OLD.livro_id;
    END;
"""

call_data_devolucao = """
    CREATE TRIGGER IF NOT EXISTS before_insert_emprestimo
    BEFORE INSERT ON emprestimo
    FOR EACH ROW
    BEGIN
        DECLARE data_devolucao DATE;
        CALL calcular_data_devolucao(data_devolucao);
    SET NEW.data_devolucao = data_devolucao;
    END;
"""