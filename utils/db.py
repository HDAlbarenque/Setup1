import os
from datetime import date
from typing import Optional

from sqlalchemy import Column, Date, Integer, String, create_engine, text, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker


DB_FILENAME = "Setup.db"
DB_URL = f"sqlite:///{DB_FILENAME}"


Base = declarative_base()


class TMPActividades(Base):
    __tablename__ = "TMP_Actividades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_responsable = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=True)
    numero_act = Column(Integer, nullable=True)
    asunto = Column(String(512), nullable=True)
    horas = Column(String(16), nullable=True)  # Formato HH:MM:SS


class TMPActividadesDario(Base):
    __tablename__ = "TMP_Actividades_Dario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(String(2), nullable=True)
    numero = Column(Integer, nullable=True)
    nombre = Column(Text, nullable=True)
    comienzo = Column(DateTime, nullable=True)
    fin = Column(DateTime, nullable=True)
    sintesis = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    vcx_s = Column(Text, nullable=True)
    req_sincro = Column(Text, nullable=True)
    version = Column(Text, nullable=True)
    numero_responsable = Column(Integer, nullable=False)


def get_engine():
    os.makedirs(os.getcwd(), exist_ok=True)
    engine = create_engine(DB_URL, future=True)
    return engine


def get_session_factory():
    engine = get_engine()
    # Asegurar esquema de tabla temporal si existe con tipos antiguos
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("PRAGMA table_info('TMP_Actividades')")).fetchall()
            if rows:
                numero_act_info = None
                for row in rows:
                    # PRAGMA table_info: (cid, name, type, notnull, dflt_value, pk)
                    if row[1] == "numero_act":
                        numero_act_info = row
                        break
                if numero_act_info is not None and str(numero_act_info[2]).upper() != "INTEGER":
                    conn.execute(text("DROP TABLE IF EXISTS TMP_Actividades"))
                    conn.commit()
    except Exception:
        # En caso de error, continuar y dejar que create_all maneje lo posible
        pass
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


