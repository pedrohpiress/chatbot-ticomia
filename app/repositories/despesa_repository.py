# repositories/despesa_repository.py

from typing import List, Dict, Optional
from sqlalchemy import text
from app.core.database import get_engine


class DespesaRepository:

    def __init__(self):
        self.engine = get_engine()

    def listar_despesas(self, limit: int = 5) -> List[Dict]:
        query = text("""
            SELECT
                d.id,
                d.descricao,
                d.valor_total AS valor,
                d.valor_pago,
                d.saldo_restante,
                d.status,
                d.data_vencimento,
                f.nome AS fornecedor,
                e.nome AS evento
            FROM despesas d
            LEFT JOIN fornecedores f ON f.id = d.fornecedor_id
            LEFT JOIN eventos e ON e.id = d.evento_id
            ORDER BY d.valor_total DESC
            LIMIT :limit
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"limit": limit})
            return [dict(row._mapping) for row in result]

    def listar_despesas_pendentes(self, limit: int = 10) -> List[Dict]:
        query = text("""
            SELECT
                d.id,
                d.descricao,
                d.valor_total AS valor,
                d.data_vencimento,
                f.nome AS fornecedor,
                e.nome AS evento
            FROM despesas d
            LEFT JOIN fornecedores f ON f.id = d.fornecedor_id
            LEFT JOIN eventos e ON e.id = d.evento_id
            WHERE d.status IN ('ABERTA', 'PARCIAL')
            ORDER BY d.data_vencimento ASC
            LIMIT :limit
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"limit": limit})
            return [dict(row._mapping) for row in result]

    def listar_despesas_pagas(self, limit: int = 10) -> List[Dict]:
        query = text("""
            SELECT
                d.id,
                d.descricao,
                d.valor_total AS valor,
                d.valor_pago,
                d.saldo_restante,
                d.data_vencimento,
                f.nome AS fornecedor,
                e.nome AS evento
            FROM despesas d
            LEFT JOIN fornecedores f ON f.id = d.fornecedor_id
            LEFT JOIN eventos e ON e.id = d.evento_id
            WHERE d.status = 'QUITADA'
            ORDER BY d.updated_at DESC
            LIMIT :limit
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"limit": limit})
            return [dict(row._mapping) for row in result]

    def buscar_por_id(self, despesa_id: int) -> Optional[Dict]:
        query = text("""
            SELECT
                d.*,
                f.nome AS fornecedor,
                e.nome AS evento
            FROM despesas d
            LEFT JOIN fornecedores f ON f.id = d.fornecedor_id
            LEFT JOIN eventos e ON e.id = d.evento_id
            WHERE d.id = :id
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"id": despesa_id}).fetchone()

            if not result:
                return None

            return dict(result._mapping)

    def listar_por_conta(self, conta_id: int, limit: int = 10) -> List[Dict]:
        query = text("""
            SELECT
                d.id,
                d.descricao,
                d.valor_total AS valor,
                d.valor_pago,
                d.saldo_restante,
                d.status,
                d.data_vencimento,
                pd.data_pagamento,
                pd.valor AS valor_pago_registro,
                f.nome AS fornecedor
            FROM pagamentos_despesa pd
            INNER JOIN despesas d ON d.id = pd.despesa_id
            LEFT JOIN fornecedores f ON f.id = d.fornecedor_id
            WHERE pd.conta_id = :conta_id
            ORDER BY data_vencimento DESC
            LIMIT :limit
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"conta_id": conta_id, "limit": limit})
            return [dict(row._mapping) for row in result]

    def listar_por_fornecedor(self, fornecedor_id: int, limit: int = 10) -> List[Dict]:
        query = text("""
            SELECT
                id,
                descricao,
                valor_total AS valor,
                valor_pago,
                saldo_restante,
                status,
                data_vencimento
            FROM despesas
            WHERE fornecedor_id = :fornecedor_id
            ORDER BY data_vencimento DESC
            LIMIT :limit
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"fornecedor_id": fornecedor_id, "limit": limit})
            return [dict(row._mapping) for row in result]


def listar_despesas(limit: int = 5):
    return DespesaRepository().listar_despesas(limit)