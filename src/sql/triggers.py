incremente_exemplar = """
    CREATE TRIGGER incrementar_quantidade_exemplares
    AFTER INSERT ON exemplares
    FOR EACH ROW
    BEGIN
        UPDATE livro
        SET quantidade_exemplares = quantidade_exemplares + 1
        WHERE id = NEW.livro_id;
    END;
"""

decrementa_exemplar = """
    CREATE TRIGGER decrementar_quantidade_exemplares
    AFTER DELETE ON exemplares
    FOR EACH ROW
    BEGIN
        UPDATE livro
        SET quantidade_exemplares = quantidade_exemplares - 1
        WHERE id = OLD.livro_id;
    END;
"""