"""
Modelo de Usuario optimizado para MySQL en producción.
"""

from typing import Optional
from datetime import datetime
import bcrypt
from sqlalchemy import String, Text, Boolean, DateTime, Integer, Index
from sqlalchemy.orm import Session, relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.config.database import Base


class User(Base):
    """
    Modelo de Usuario optimizado para MySQL en producción.
    
    Esta clase define la estructura de la entidad usuario e incluye métodos para
    autenticación, gestión de contraseñas y operaciones de base de datos optimizadas.

    Atributos:
        id: Identificador único del usuario (clave primaria)
        username: Nombre de usuario único (opcional)
        email: Correo electrónico único (requerido)
        password: Contraseña hasheada con bcrypt
        nombre: Nombre completo del usuario
        apellidos: Apellidos del usuario
        avatar_url: URL del avatar del usuario
        is_active: Estado del usuario (activo/inactivo)
        is_verified: Indica si el email está verificado
        last_login: Fecha y hora del último acceso
        login_attempts: Número de intentos de login fallidos
        created_at: Fecha y hora de creación
        updated_at: Fecha y hora de última actualización
        
    Métodos:
        authenticate: Autenticar usuario con email y contraseña
        create_password: Crear hash de contraseña
        is_account_locked: Verificar si la cuenta está bloqueada
        reset_login_attempts: Resetear intentos de login
        increment_login_attempts: Incrementar intentos de login
    """
    
    __tablename__ = 'users'
    
    
    # Configuración específica para MySQL
    __table_args__ = (
        # Índices compuestos para consultas frecuentes
        Index('idx_email_active', 'email', 'is_active'),
        Index('idx_username_active', 'username', 'is_active'),
        Index('idx_created_at', 'created_at'),
        Index('idx_last_login', 'last_login'),
        
        # Configuración de MySQL
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci',
            'mysql_row_format': 'DYNAMIC',
            'extend_existing': True 
        }
    )

    # Clave primaria
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único del usuario"
    )
    
    # Campos de identificación
    username: Mapped[Optional[str]] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=True,
        comment="Nombre de usuario único"
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="Correo electrónico único del usuario"
    )
    
    # Seguridad
    password: Mapped[str] = mapped_column(
        String(255),  # Suficiente para hash bcrypt
        nullable=False,
        comment="Contraseña hasheada con bcrypt"
    )
    
    # Información personal
    nombre: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="Nombre del usuario"
    )
    
    apellidos: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="Apellidos del usuario"
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(
        Text,  # URLs pueden ser largas
        nullable=True,
        comment="URL del avatar del usuario"
    )
    
    # Estados y control
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Estado activo del usuario"
    )
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Indica si el email está verificado"
    )
    
    # Seguridad y auditoría
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="Fecha y hora del último acceso"
    )
    
    login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Número de intentos de login fallidos"
    )
    
    # Timestamps automáticos
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),    
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Fecha y hora de creación"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Fecha y hora de última actualización"
    )

    # Relaciones
    pets = relationship(
        "Pet", 
        back_populates="owner", 
        cascade="all, delete-orphan",
        lazy="select"  # Optimización para MySQL
    )

    @classmethod
    def authenticate(cls, db: Session, email: str, password: str) -> Optional["User"]:
        """
        Autentica un usuario por email y contraseña.
        
        Args:
            db: Sesión de base de datos
            email: Correo electrónico del usuario
            password: Contraseña en texto plano
            
        Returns:
            Usuario autenticado o None si falla la autenticación
        """
        # Buscar usuario activo por email
        user = db.query(cls).filter(
            cls.email == email,
            cls.is_active == True
        ).first()
        
        if not user:
            return None
            
        # Verificar si la cuenta está bloqueada
        if user.is_account_locked():
            return None
            
        # Verificar contraseña
        if user.check_password(password):
            # Resetear intentos de login y actualizar último acceso
            user.reset_login_attempts()
            user.last_login = datetime.now()
            db.commit()
            return user
        else:
            # Incrementar intentos fallidos
            user.increment_login_attempts()
            db.commit()
            return None

    @classmethod
    def create_password(cls, password: str) -> str:
        """
        Crea un hash de contraseña usando bcrypt.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Contraseña hasheada
        """
        # Usar un costo de 12 para producción (balance seguridad/rendimiento)
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt(rounds=12)
        )
        return hashed_password.decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """
        Verifica si una contraseña coincide con el hash almacenado.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                self.password.encode('utf-8')
            )
        except Exception:
            return False
    
    def is_account_locked(self) -> bool:
        """
        Verifica si la cuenta está bloqueada por intentos fallidos.
        
        Returns:
            True si la cuenta está bloqueada, False en caso contrario
        """
        MAX_LOGIN_ATTEMPTS = 5
        return self.login_attempts >= MAX_LOGIN_ATTEMPTS
    
    def reset_login_attempts(self) -> None:
        """Resetea el contador de intentos de login fallidos."""
        self.login_attempts = 0
    
    def increment_login_attempts(self) -> None:
        """Incrementa el contador de intentos de login fallidos."""
        self.login_attempts += 1
    
    @property
    def nombre_completo(self) -> str:
        """
        Retorna el nombre completo del usuario.
        
        Returns:
            Nombre completo concatenado
        """
        parts = []
        if self.nombre:
            parts.append(self.nombre)
        if self.apellidos:
            parts.append(self.apellidos)
        return " ".join(parts) if parts else self.email
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convierte el usuario a diccionario.
        
        Args:
            include_sensitive: Incluir campos sensibles como password
            
        Returns:
            Diccionario con los datos del usuario
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'nombre_completo': self.nombre_completo,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            data.update({
                'login_attempts': self.login_attempts,
                'is_account_locked': self.is_account_locked()
            })
            
        return data

    """
    El método __repr__ define cómo se representa textualmente un objeto cuando se imprime o se muestra en el debugger. Su propósito principal es proporcionar una representación clara y útil del objeto para desarrolladores durante el debugging y logging. 
    Cumple el mismo rol que toString() en Java: hacer que los objetos se muestren de forma legible en lugar de como referencias de memoria.
    En este caso específico:

    Identifica el objeto: Muestra el ID y un identificador (username o email)
    Facilita el debugging: Cuando imprimes el objeto, ves información útil en lugar de algo como <__main__.Usuario object at 0x7f8b8c0d5f40>
    Mejora el logging: Los logs muestran información legible del usuario
    Ayuda en desarrollo: En consolas interactivas y debuggers, puedes identificar rápidamente qué objeto estás manejando
    """
    def __repr__(self) -> str:
        """Representación string del objeto Usuario."""
        identifier = self.username or self.email
        return f"<Usuario(id={self.id}, identifier='{identifier}', active={self.is_active})>"