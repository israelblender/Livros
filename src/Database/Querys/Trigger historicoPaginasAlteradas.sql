CREATE trigger 
--IF NOT exists 
historicoPaginasAlteradas
after update on livros
when old.pagina_pausada <> new.pagina_pausada
begin
insert into
monitorados (
id_livro,
paginas_lidas,
data)
values (
old.id,
new.pagina_pausada - old.pagina_pausada,
datetime('NOW')
);
END;