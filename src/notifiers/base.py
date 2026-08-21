# -*- coding: utf-8 -*-
"""
OpenSentinel Base Notifier Abstract Class
Defines the standard interface for all alert providers (Discord, Telegram, WhatsApp, etc.)
"""

from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.name = self.__class__.__name__

    @abstractmethod
    def is_enabled(self) -> bool:
        """Verifica si el canal está configurado y habilitado."""
        pass

    @abstractmethod
    def send_boot_alert(self, hw: dict, net: dict) -> bool:
        """Envía la alerta de inicio de sesión / encendido del sistema."""
        pass

    @abstractmethod
    def send_evidence_alert(self, img_bytes: bytes, title: str, reason: str) -> bool:
        """Envía una foto de evidencia forense o captura de seguridad."""
        pass

    @abstractmethod
    def send_test_message(self) -> dict:
        """Envía un mensaje de prueba para verificar conectividad."""
        pass
