# Siglent SPD3303X-E and SPD3303X power supply drivers
# Sébastien Deriaz
# 02.04.2023


from syndesi.protocols import SCPI, Protocol
from . import MultiChannelPowersupplyDC, PowersupplyDC
from ..scpi_driver import SCPIDriver
from syndesi.adapters import *
from packaging.version import Version
from typing import Union
from enum import Enum
from syndesi.tools.types import assert_number, is_number
from dataclasses import dataclass
import struct

DEFAULT_TIMEOUT = Timeout(0.2, 0.1)


class ChannelMode(Enum):
    CONSTANT_VOLTAGE = 0
    CONSTANT_CURRENT = 1


class OperationMode(Enum):
    INDEPENDENT = 'independant'
    SERIES = 'series'
    PARALLEL = 'parallel'


_operation_mode_id = {
    OperationMode.INDEPENDENT: 0,
    OperationMode.SERIES: 1,
    OperationMode.PARALLEL: 2
}


@dataclass
class SystemStatus:
    channel1_mode: ChannelMode
    channel2_mode: ChannelMode
    operation_mode: OperationMode
    channel1_enabled: bool
    channel2_enabled: bool
    timer1_enabled: bool
    timer2_enabled: bool
    channel1_waveform_display: bool
    channel2_waveform_display: bool


class SiglentSPD3303xChannel(PowersupplyDC):
    VERSION = Version('1.0.0')

    def __init__(self, adapter: Union[Adapter, Protocol], channel_number: int = None) -> None:
        super().__init__(channel_number)
        if isinstance(adapter, Protocol):
            self._prot = adapter
        else:
            adapter.set_default_timeout(DEFAULT_TIMEOUT)
            self._prot = SCPI(adapter)

    def measure_dc_current(self) -> float:
        """
        Return current measurement
        
        Status : ok

        Returns
        -------
        current : float
        """
        output = self._prot.query(f'MEAS:CURR? CH{self._channel_number}')
        return float(output)

    def measure_dc_voltage(self) -> float:
        """
        Return voltage measurement

        Status : ok

        Returns
        -------
        voltage : float
        """
        output = self._prot.query(f'MEAS:VOLT? CH{self._channel_number}')
        return float(output)

    def measure_dc_power(self) -> float:
        """
        Return power measurement

        Status : ok

        Returns
        -------
        power : float
        """
        output = self._prot.query(f'MEAS:POWE? CH{self._channel_number}')
        return float(output)

    def set_voltage(self, volts: float):
        """
        
        Status : ok
        """
        self._prot.write(f'CH{self._channel_number}:VOLT {volts:.3f}')

    def get_voltage(self) -> float:
        """
        
        Status : ok
        """
        self._prot.write(f'CH{self._channel_number}:VOLT?')
        output = self._prot.read()
        try:
            volts = float(output)
        except ValueError as e:
            volts = None
        return volts

    def set_current(self, amps: float):
        """
        
        Status : ok
        """
        self._prot.write(f'CH{self._channel_number}:CURR {amps:.3f}')

    def get_current(self) -> float:
        """
        
        Status : ok
        """
        self._prot.write(f'CH{self._channel_number}:CURR?')
        output = self._prot.read()
        try:
            amps = float(output)
        except ValueError as e:
            amps = None
        return amps

    def set_output_state(self, state: bool):
        self._prot.write(
            f'OUTP CH{self._channel_number},{"ON" if state else "OFF"}')

    def set_wave_display(self, state: bool):
        """
        Enable/disable the wave display

        Status : ok

        Parameters
        ----------
        state : bool
        """
        self._prot.write(
            f'OUTP:WAVE CH{self._channel_number},{"ON" if state else "OFF"}')

    def set_timer(self, group, voltage, current, time):
        """
        Set timing parameters, including group(1-5), voltage, current and time

        Status : ok

        Parameters
        ----------
        voltage : float or list
        current : float or list
        time : float or list
        """
        if all([is_number(x) for x in [group, voltage, current, time]]):
            # Make lists
            group = [group]
            voltage = [voltage]
            current = [current]
            time = [time]
        elif not all([isinstance(x, list) for x in [group, voltage, current, time]]):
            raise ValueError(f"Invalid input types")

        for g, v, c, t in zip(group, voltage, current, time):
            assert 1 <= g <= 5, f'Invalid group value : {g}'
            self._prot.write(
                f'TIME:SET CH{self._channel_number},{g},{v},{c},{t}')

    def get_timer(self, group):
        """
        Query the voltage/current/time parameters of specified group

        Status : ok

        Parameters
        ----------
        group : int

        Returns
        -------
        voltage : float
        current : float
        time : float
        """
        assert_number(group)
        output = self._prot.query(
            f'TIME:SET? CH{self._channel_number},{group}')
        voltage, current, time = [float(x) for x in output.split(',') if x]
        return voltage, current, time

    def get_mode(self):
        """
        Return channel mode (constant voltage or constant current)

        Status : ok

        Returns
        -------
        mode : ChannelMode
        """
        code = int(self._prot.query('SYST:STAT?'), 16)

        mask = (0b0000000001 << (self._channel_number-1))

        mode = ChannelMode.CONSTANT_CURRENT if (
            code & mask) else ChannelMode.CONSTANT_VOLTAGE

        return mode


class SiglentSPD3303x(MultiChannelPowersupplyDC, SCPIDriver):
    VERSION = Version('1.0.0')

    def __init__(self, adapter: Adapter) -> None:
        # TODO : Check if this is the right way
        MultiChannelPowersupplyDC.__init__(self, 2)
        assert isinstance(adapter, VISA) or isinstance(
            adapter, IP), "Invalid adapter"
        # TODO : Check if this is the right way
        SCPIDriver.__init__(self, adapter)

    def test(self):
        return 'SPD3303X' in self.get_identification()

    def channel(self, channel_number: int) -> SiglentSPD3303xChannel:
        return SiglentSPD3303xChannel(self._prot, channel_number=channel_number)

    def set_operation_mode(self, mode: OperationMode):
        """
        Set the operation mode

        Status : ok

        Parameters
        ----------
        mode : OperationMode or str
            'independant', 'series' or 'parallel'
        """
        mode = OperationMode(mode)
        _id = _operation_mode_id[mode]
        self._prot.write(f'OUTP:TRACK {_id}')

    def _check_save_id(self, save_id: int):
        assert_number(save_id)
        assert 1 <= save_id <= 5, f'Invalid save_id value : {save_id}'

    def save(self, save_id: int):
        """
        Save current state in nonvolatile memory

        Status : ok

        Parameters
        ----------
        save_id : int
            Save index [1-5]
        """
        self._check_save_id(save_id)
        self._prot.write(f'*SAV {save_id}')

    def recall(self, save_id: int):
        """
        Recall state that had been saved from nonvolatile memory

        Status : ok

        Parameters
        ----------
        save_id : int
            Save index [1-5]
        """
        self._check_save_id(save_id)
        self._prot.write(f'*RCL {save_id}')

    def select_instrument_channel(self, channel_number: int):
        """
        Select the channel that will be operated. This is not necessary to use either channel with this driver

        Status : ok

        Parameters
        ----------
        channel_number : int
        """
        self._check_channel(channel_number)
        self._prot.write(f'INST CH{channel_number}')

    def get_instrument_channel(self):
        """
        Return the selected channel

        Status : ok

        Returns
        -------
        channel_number : int
        """
        # output : CHx
        output = self._prot.query('INST?')
        channel_number = int(output.strip('CH'))
        return channel_number

    def measure_total_dc_power(self):
        """
        Return sum of both channel power

        Status : ok

        Returns
        -------
        power : float
        """
        output = sum([self.channel(i+1).measure_dc_power()
                     for i in range(self._n_channels)])
        return output

    def get_system_status(self):
        """
        Query the current working state of the equipment

        Status : ok

        Returns
        -------
        status : SystemStatus
        """
        code = int(self._prot.query('SYST:STAT?'), 16)

        operation_mode = {
            0b01: OperationMode.INDEPENDENT,
            0b10: OperationMode.PARALLEL,
            0b11: OperationMode.SERIES
        }
        status = SystemStatus(
            channel1_mode=ChannelMode.CONSTANT_CURRENT if (
                code & 0b0000000001) else ChannelMode.CONSTANT_VOLTAGE,
            channel2_mode=ChannelMode.CONSTANT_CURRENT if (
                code & 0x0000000010) else ChannelMode.CONSTANT_VOLTAGE,
            operation_mode=operation_mode[(code >> 2) & 0b11],
            channel1_enabled=bool(code & 0b0000010000),
            channel2_enabled=bool(code & 0b0000100000),
            timer1_enabled=bool(code & 0b0001000000),
            timer2_enabled=bool(code & 0b0010000000),
            channel1_waveform_display=bool(code & 0b0100000000),
            channel2_waveform_display=bool(code & 0b1000000000)
        )
        return status

    def get_ip_address(self):
        """
        Return IP address

        Status : ok

        Returns
        -------
        ip : str
        """
        return self._prot.query('IP?')

    def set_ip_address(self, ip: str):
        """
        Set IP address. This command is invalid when DHCP is enabled

        Status : ok

        Parameters
        ----------
        ip : str
            format 192.168.1.1        
        """
        self._prot.write(f'IP {ip}')

    def get_subnet_mask(self):
        """
        Return subnet mask

        Status : ok

        Returns
        -------
        mask : str
        """
        return self._prot.query('MASK?')

    def set_subnet_mask(self, mask: str):
        """
        Set subnet mask

        Status : ok

        Parameters
        ----------
        mask : str
        """
        self._prot.write(f'MASK {mask}')

    def get_gateway(self):
        """
        Return gateway

        Status : ok

        Returns
        ----------
        gateway : str
        """
        return self._prot.query('GATE?')

    def set_gateway(self, gateway: str):
        """
        Set gateway

        Status : ok

        Parameters
        ----------
        gateway : str
        """
        self._prot.write(f'GATE {gateway}')

    def get_dhcp(self):
        """
        Return DHCP status

        Status : ok

        Returns
        -------
        dhcp : bool
        """
        value = self._prot.query('DHCP?')
        return 'on' in value.lower()

    def set_dhcp(self, dhcp: bool):
        """
        Set DHCP status

        Status : ok

        Parameters
        ----------
        dhcp : bool
        """
        self._prot.write(f'DHCP {"ON" if dhcp else "OFF"}')
