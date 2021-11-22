"""Test the update coordinator for HomeWizard Energy."""

from unittest.mock import patch

from homeassistant.components.homewizard_energy.const import (
    ATTR_ACTIVE_POWER_L1_W,
    ATTR_ACTIVE_POWER_L2_W,
    ATTR_ACTIVE_POWER_L3_W,
    ATTR_ACTIVE_POWER_W,
    ATTR_GAS_TIMESTAMP,
    ATTR_METER_MODEL,
    ATTR_SMR_VERSION,
    ATTR_TOTAL_ENERGY_EXPORT_T1_KWH,
    ATTR_TOTAL_ENERGY_EXPORT_T2_KWH,
    ATTR_TOTAL_ENERGY_IMPORT_T1_KWH,
    ATTR_TOTAL_ENERGY_IMPORT_T2_KWH,
    ATTR_TOTAL_GAS_M3,
    ATTR_WIFI_SSID,
    ATTR_WIFI_STRENGTH,
)
from homeassistant.components.sensor import (
    ATTR_STATE_CLASS,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_FRIENDLY_NAME,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TIMESTAMP,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
    POWER_WATT,
    VOLUME_CUBIC_METERS,
)
from homeassistant.helpers import entity_registry as er

from .generator import get_mock_device


async def test_sensor_entity_smr_version(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads smr version."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_SMR_VERSION,
    ]
    api.data.smr_version = 50

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_smr_version")
    entry = entity_registry.async_get("sensor.custom_name_smr_version")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_smr_version"
    assert not entry.disabled
    assert state.state == "50"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name SMR Version"
    assert ATTR_STATE_CLASS not in state.attributes
    assert ATTR_UNIT_OF_MEASUREMENT not in state.attributes
    assert ATTR_DEVICE_CLASS not in state.attributes
    assert state.attributes.get(ATTR_ICON) == "mdi:wifi"


async def test_sensor_entity_meter_model(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads meter model."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_METER_MODEL,
    ]
    api.data.meter_model = "Model X"

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_model")
    entry = entity_registry.async_get("sensor.custom_name_model")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_meter_model"
    assert not entry.disabled
    assert state.state == "Model X"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Model"
    assert ATTR_STATE_CLASS not in state.attributes
    assert ATTR_UNIT_OF_MEASUREMENT not in state.attributes
    assert ATTR_DEVICE_CLASS not in state.attributes
    assert state.attributes.get(ATTR_ICON) == "mdi:counter"


async def test_sensor_entity_wifi_ssid(hass, mock_config_entry_data, mock_config_entry):
    """Test entity loads wifi ssid."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_WIFI_SSID,
    ]
    api.data.wifi_ssid = "My Wifi"

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_wifi_ssid")
    entry = entity_registry.async_get("sensor.custom_name_wifi_ssid")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_wifi_ssid"
    assert not entry.disabled
    assert state.state == "My Wifi"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Wifi SSID"
    assert ATTR_STATE_CLASS not in state.attributes
    assert ATTR_UNIT_OF_MEASUREMENT not in state.attributes
    assert ATTR_DEVICE_CLASS not in state.attributes
    assert state.attributes.get(ATTR_ICON) == "mdi:wifi"


async def test_sensor_entity_wifi_strength(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads wifi strength."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_WIFI_STRENGTH,
    ]
    api.data.wifi_strength = 42

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_wifi_strength")
    entry = entity_registry.async_get("sensor.custom_name_wifi_strength")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_wifi_strength"
    assert not entry.disabled
    assert state.state == "42"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Wifi Strength"
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE
    assert ATTR_DEVICE_CLASS not in state.attributes
    assert state.attributes.get(ATTR_ICON) == "mdi:wifi"


async def test_sensor_entity_total_power_import_t1_kwh(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads total power import t1."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_TOTAL_ENERGY_IMPORT_T1_KWH,
    ]
    api.data.total_power_import_t1_kwh = 1234.123

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_total_power_import_t1")
    entry = entity_registry.async_get("sensor.custom_name_total_power_import_t1")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_total_power_import_t1_kwh"
    assert not entry.disabled
    assert state.state == "1234.123"
    assert (
        state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Total Power Import T1"
    )
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_ENERGY
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_total_power_import_t2_kwh(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads total power import t2."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_TOTAL_ENERGY_IMPORT_T2_KWH,
    ]
    api.data.total_power_import_t2_kwh = 1234.123

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_total_power_import_t2")
    entry = entity_registry.async_get("sensor.custom_name_total_power_import_t2")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_total_power_import_t2_kwh"
    assert not entry.disabled
    assert state.state == "1234.123"
    assert (
        state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Total Power Import T2"
    )
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_ENERGY
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_total_power_export_t1_kwh(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads total power export t1."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_TOTAL_ENERGY_EXPORT_T1_KWH,
    ]
    api.data.total_power_export_t1_kwh = 1234.123

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_total_power_export_t1")
    entry = entity_registry.async_get("sensor.custom_name_total_power_export_t1")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_total_power_export_t1_kwh"
    assert not entry.disabled
    assert state.state == "1234.123"
    assert (
        state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Total Power Export T1"
    )
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_ENERGY
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_total_power_export_t2_kwh(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads total power export t2."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_TOTAL_ENERGY_EXPORT_T2_KWH,
    ]
    api.data.total_power_export_t2_kwh = 1234.123

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_total_power_export_t2")
    entry = entity_registry.async_get("sensor.custom_name_total_power_export_t2")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_total_power_export_t2_kwh"
    assert not entry.disabled
    assert state.state == "1234.123"
    assert (
        state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Total Power Export T2"
    )
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == ENERGY_KILO_WATT_HOUR
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_ENERGY
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_active_power(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads active power."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_ACTIVE_POWER_W,
    ]
    api.data.active_power_w = 123.123

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_active_power")
    entry = entity_registry.async_get("sensor.custom_name_active_power")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_active_power_w"
    assert not entry.disabled
    assert state.state == "123.123"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Active Power"
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_POWER
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_active_power_l1(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads active power l1."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_ACTIVE_POWER_L1_W,
    ]
    api.data.active_power_l1_w = 123.123

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_active_power_l1")
    entry = entity_registry.async_get("sensor.custom_name_active_power_l1")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_active_power_l1_w"
    assert not entry.disabled
    assert state.state == "123.123"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Active Power L1"
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_POWER
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_active_power_l2(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads active power l2."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_ACTIVE_POWER_L2_W,
    ]
    api.data.active_power_l2_w = 456.456

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_active_power_l2")
    entry = entity_registry.async_get("sensor.custom_name_active_power_l2")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_active_power_l2_w"
    assert not entry.disabled
    assert state.state == "456.456"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Active Power L2"
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_POWER
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_active_power_l3(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads active power l3."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_ACTIVE_POWER_L3_W,
    ]
    api.data.active_power_l3_w = 789.789

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_active_power_l3")
    entry = entity_registry.async_get("sensor.custom_name_active_power_l3")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_active_power_l3_w"
    assert not entry.disabled
    assert state.state == "789.789"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Active Power L3"
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_MEASUREMENT
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == POWER_WATT
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_POWER
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_total_gas(hass, mock_config_entry_data, mock_config_entry):
    """Test entity loads total gas."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_TOTAL_GAS_M3,
    ]
    api.data.total_gas_m3 = 50

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_total_gas")
    entry = entity_registry.async_get("sensor.custom_name_total_gas")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_total_gas_m3"
    assert not entry.disabled
    assert state.state == "50"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Total Gas"
    assert state.attributes.get(ATTR_STATE_CLASS) == STATE_CLASS_TOTAL_INCREASING
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == VOLUME_CUBIC_METERS
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_GAS
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_gas_timestamp(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test entity loads gas timestamp."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_GAS_TIMESTAMP,
    ]
    api.data.gas_timestamp = 50

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    state = hass.states.get("sensor.custom_name_gas_timestamp")
    entry = entity_registry.async_get("sensor.custom_name_gas_timestamp")
    assert entry
    assert state
    assert entry.unique_id == "aabbccddeeff_gas_timestamp"
    assert not entry.disabled
    assert state.state == "50"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Custom Name Gas Timestamp"
    assert ATTR_STATE_CLASS not in state.attributes
    assert ATTR_UNIT_OF_MEASUREMENT not in state.attributes
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_TIMESTAMP
    assert ATTR_ICON not in state.attributes


async def test_sensor_entity_disabled_when_null(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test sensor disables data with null by default."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_ACTIVE_POWER_L2_W,
        ATTR_ACTIVE_POWER_L3_W,
        ATTR_TOTAL_GAS_M3,
        ATTR_GAS_TIMESTAMP,
    ]
    api.data.active_power_l2_w = None
    api.data.active_power_l3_w = None
    api.data.total_gas_m3 = None
    api.data.gas_timestamp = None

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("sensor.custom_name_active_power_l2")
    assert entry
    assert entry.disabled

    entry = entity_registry.async_get("sensor.custom_name_active_power_l3")
    assert entry
    assert entry.disabled

    entry = entity_registry.async_get("sensor.custom_name_total_gas")
    assert entry
    assert entry.disabled

    entry = entity_registry.async_get("sensor.custom_name_gas_timestamp")
    assert entry
    assert entry.disabled


async def test_sensor_entity_export_disabled_when_unused(
    hass, mock_config_entry_data, mock_config_entry
):
    """Test sensor disables export if value is 0."""

    api = get_mock_device()
    api.data.available_datapoints = [
        ATTR_TOTAL_ENERGY_EXPORT_T1_KWH,
        ATTR_TOTAL_ENERGY_EXPORT_T2_KWH,
    ]
    api.data.total_power_export_t1_kwh = 0
    api.data.total_power_export_t2_kwh = 0

    with patch(
        "aiohwenergy.HomeWizardEnergy",
        return_value=api,
    ):
        entry = mock_config_entry
        entry.data = mock_config_entry_data
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("sensor.custom_name_total_power_export_t1")
    assert entry
    assert entry.disabled

    entry = entity_registry.async_get("sensor.custom_name_total_power_export_t2")
    assert entry
    assert entry.disabled
