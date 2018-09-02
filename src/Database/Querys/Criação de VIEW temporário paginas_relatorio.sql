CREATE TEMPORARY VIEW paginas_relatorio AS select id, total_paginas, pagina_pausada, total_paginas - pagina_pausada
 AS paginas_restantes
 FROM livros ORDER BY total_paginas DESC