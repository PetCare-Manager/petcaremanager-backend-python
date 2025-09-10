"""Tests para la configuración del engine de base de datos"""
import pytest
from config.database_config import DatabaseConfig
from config.enums import Entorno


class TestConfigEngine:
    """Tests para obtener_config_engine()"""
    
    def test_mysql_config_has_pool_settings(self, monkeypatch):
        """Verificar que MySQL tiene configuración de pool"""
        # Simular entorno de producción
        monkeypatch.setenv("Entorno", "produccion")
        monkeypatch.setenv("USE_MYSQL", "true")
        
        config = DatabaseConfig()
        engine_config = config.obtener_config_engine()
        
        # Verificar configuración del pool
        assert "pool_size" in engine_config
        assert "max_overflow" in engine_config
        assert "pool_timeout" in engine_config
        assert "pool_recycle" in engine_config
        assert "pool_pre_ping" in engine_config
        
    def test_echo_true_in_desarrollo(self, monkeypatch):
        """Verificar echo=True en desarrollo"""
        monkeypatch.setenv("Entorno", "desarrollo")
        
        config = DatabaseConfig()
        engine_config = config.obtener_config_engine()
        
        assert engine_config["echo"] is True
        
    def test_echo_false_in_produccion(self, monkeypatch):
        """Verificar echo=False en producción"""
        monkeypatch.setenv("Entorno", "produccion")
        
        config = DatabaseConfig()
        engine_config = config.obtener_config_engine()
        
        assert engine_config["echo"] is False