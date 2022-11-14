"""Platform for integrating a Simple Altering Light."""
from __future__ import annotations
from typing import Any, Final
import gc
import time

# Import the device class from the component that you want to support
from homeassistant.core import HomeAssistant
from homeassistant.components.light import LightEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Adding the Simple Altering light to Home Assistant."""

    add_entities([LightAlteringState()])
    return True


class LightAlteringState(LightEntity):
    """A Light able to modify other components"""

    _target: Final[str] = "switch.switch_target"

    def __init__(self) -> None:
        """Initialize a LightAlteringState."""
        self._name = "Simple Altering"
        self._brightness = None
        self._state = False

        # This object should physically communicate with the light
        self._light = LightEntity()

        print('Light "' + self._name + '" was created.')

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._brightness = 255
        self._state = True
        self.alter_values()

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._brightness = 0
        self._state = False
        self.alter_values()

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        # self._light.update()
        # self._state = self._light.is_on()
        # self._brightness = self._light.brightness
        return

    def alter_values(self):
        """This method alter the state of a target integrations."""
        
        t_state = self.hass.states.get(self._target)
        print(self._target + " - actual state: " + t_state.state)

        # Updating the value accessing the integration instance through the Garbage Collector
        obj = self._get_target("Switch Target")
        if obj:
            obj.toggle()
        else:
            print("Switch Target not found!")

        # Waiting for update
        time.sleep(2)

        # Printing new updated state
        t_state = self.hass.states.get(self._target)
        print(self._target + " actual state: " + t_state.state)

        return True
    
    def _get_target(self, target_name: str):
        """Getting an integration reference through the Garbage Collector"""

        for obj in gc.get_objects():
            if isinstance(obj, SwitchEntity):
                if obj.name == target_name:
                    print(target_name + " found!")
                    return obj

        return False
