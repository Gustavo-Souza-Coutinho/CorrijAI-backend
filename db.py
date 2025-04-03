import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        with self.conn:
            # Tabela para usuários (professores e alunos)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                flg_tipo TEXT NOT NULL CHECK(flg_tipo IN ('P', 'A'))
            )
            """)
            # Tabela para perguntas
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS pergunta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL
            )
            """)
            # Tabela para respostas
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS resposta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pergunta INTEGER NOT NULL,
                id_aluno INTEGER NOT NULL,
                resposta TEXT NOT NULL,
                FOREIGN KEY (id_pergunta) REFERENCES pergunta (id),
                FOREIGN KEY (id_aluno) REFERENCES usuario (id)
            )
            """)
            # Nova tabela para notas dos alunos
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS nota_aluno (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_aluno INTEGER NOT NULL,
                nota INTEGER NOT NULL,
                respostas_corrigidas TEXT NOT NULL,
                data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_aluno) REFERENCES usuario (id)
            )
            """)

    def listar_perguntas(self):
        query = "SELECT * FROM pergunta"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def inserir_usuario(self, nome, email, senha, flg_tipo):
        with self.conn:
            self.conn.execute("""
            INSERT INTO usuario (nome, email, senha, flg_tipo) VALUES (?, ?, ?, ?)
            """, (nome, email, senha, flg_tipo))

    def buscar_usuario_por_email(self, email):
        cursor = self.conn.execute("""
        SELECT * FROM usuario WHERE email = ?
        """, (email,))
        return cursor.fetchone()

    def buscar_usuario_por_login(self, email, senha):
        cursor = self.conn.execute("""
        SELECT * FROM usuario WHERE email = ? AND senha = ?
        """, (email, senha))
        return cursor.fetchone()

    def buscar_professor_por_login(self, email, senha):
        cursor = self.conn.execute("""
        SELECT * FROM usuario WHERE email = ? AND senha = ? AND flg_tipo = 'P'
        """, (email, senha))
        return cursor.fetchone()

    def buscar_aluno_por_login(self, email, senha):
        cursor = self.conn.execute("""
        SELECT * FROM usuario WHERE email = ? AND senha = ? AND flg_tipo = 'A'
        """, (email, senha))
        return cursor.fetchone()

    def inserir_pergunta(self, texto):
        with self.conn:
            cursor = self.conn.execute("""
            INSERT INTO pergunta (texto) VALUES (?)
            """, (texto,))
            return cursor.lastrowid

    def atualizar_pergunta(self, id, texto):
        with self.conn:
            self.conn.execute("""
            UPDATE pergunta SET texto = ? WHERE id = ?
            """, (texto, id))

    def excluir_pergunta(self, id):
        with self.conn:
            self.conn.execute("""
            DELETE FROM pergunta WHERE id = ?
            """, (id,))

    def inserir_resposta(self, id_pergunta, id_aluno, resposta):
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO resposta (id_pergunta, id_aluno, resposta) VALUES (?, ?, ?)
                """, (id_pergunta, id_aluno, resposta))
                print(f"Resposta salva: {resposta} para pergunta ID {id_pergunta}, aluno ID {id_aluno}")
        except Exception as e:
            print(f"Erro ao salvar resposta: {e}")

    def inserir_nota_aluno(self, id_aluno, nota, respostas_corrigidas):
        with self.conn:
            cursor = self.conn.execute("""
            INSERT INTO nota_aluno (id_aluno, nota, respostas_corrigidas) VALUES (?, ?, ?)
            """, (id_aluno, nota, respostas_corrigidas))
            return cursor.lastrowid

    def listar_respostas_por_aluno(self, id_aluno):
        try:
            # Executa a consulta SQL para pegar as respostas e as perguntas associadas ao aluno
            cursor = self.conn.execute("""
            SELECT r.id, r.id_pergunta, r.resposta, p.texto AS pergunta_texto
            FROM resposta r
            JOIN pergunta p ON r.id_pergunta = p.id
            WHERE r.id_aluno = ?
            """, (id_aluno,))

            # Recupera todos os resultados
            respostas = cursor.fetchall()

            if respostas:
                # Retorna as respostas com todos os detalhes
                return [{"id": row[0], "id_pergunta": row[1], "resposta": row[2], "pergunta_texto": row[3]} for row in
                        respostas]
            else:
                # Retorna uma lista vazia se não houver respostas
                return []

        except Exception as e:
            print(f"Erro ao listar respostas: {e}")
            return []

    def listar_notas_por_aluno(self, id_aluno):
        cursor = self.conn.execute("""
        SELECT id, nota, respostas_corrigidas, data_avaliacao 
        FROM nota_aluno 
        WHERE id_aluno = ? 
        ORDER BY data_avaliacao DESC
        """, (id_aluno,))
        return cursor.fetchall()

    def listar_notas(self):
        """
        Retorna uma lista com os nomes, IDs e notas dos alunos.
        """
        cursor = self.conn.execute("""
        SELECT 
            u.id AS aluno_id, 
            u.nome AS aluno_nome, 
            n.nota AS nota 
        FROM 
            nota_aluno n 
        INNER JOIN 
            usuario u 
        ON 
            n.id_aluno = u.id 
        WHERE 
            u.flg_tipo = 'A'
        """)
        return [{"id": row[0], "nome": row[1], "nota": row[2]} for row in cursor.fetchall()]

    def listar_respostas_por_aluno(self, id_aluno):
        cursor = self.conn.execute("""
        SELECT r.id, r.id_pergunta, r.resposta, p.texto AS pergunta_texto
        FROM resposta r
        JOIN pergunta p ON r.id_pergunta = p.id
        WHERE r.id_aluno = ?
        """, (id_aluno,))

        respostas = cursor.fetchall()
        return [{"id": row[0], "id_pergunta": row[1], "resposta": row[2], "pergunta_texto": row[3]} for row in
                respostas]
